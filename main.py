#!/usr/bin/env python3
"""Demo.

https://amanxai.com/2025/12/23/langgraph-explained-from-scratch/
"""

from enum import StrEnum, auto
from typing import TypedDict, cast

from langchain_core.messages import AIMessage, HumanMessage
from langchain_ollama import ChatOllama
from langgraph.graph import END, StateGraph


class Category(StrEnum):
    math = auto()
    general = auto()


class AgentInput(TypedDict):
    messages: list[HumanMessage]


# The State dictates what data flows through the graph.
# Here, we just track the list of messages in the conversation.
class AgentState(TypedDict):
    messages: list[HumanMessage]
    category: Category


class AgentTest:
    def __init__(self) -> None:
        # Ensure you have run `ollama pull llama3` in your terminal
        self.llm = ChatOllama(model="llama3", temperature=0)

    def routing_logic(self, state: AgentState):
        # If the category is math, go to 'math_node'
        if state["category"] == "math":
            return "math_node"
        # Otherwise, go to 'general_node'
        return "general_node"

    # Node 1: The Categorizer
    def categorize_input(self, state: AgentState):
        """Analyzes the user's last message.

        decide if it's 'math' or 'general'.
        """
        last_message = state["messages"][-1].content

        # We ask the LLM to classify strictly.
        prompt = f"""
        You are a router. Classify the following input as either 'math'
        or 'General'.  Return ONLY the word 'math' or 'general'. Do not
        add punctuation.

        Input: {last_message}
        """

        response = self.llm.invoke(prompt)
        category = cast("Category", response.content).strip()

        # Update the state with the category
        return {"category": category}

    # Node 2: The Math Expert
    def handle_math(self, state: AgentState):
        print("--- 🧮 Entering Math Node ---")
        last_message = state["messages"][-1].content
        response = self.llm.invoke(
            f"You are a mathematician. Solve this simply: {last_message}"
        )
        # We append the AI's response to the message history
        return {"messages": [response]}

    # Node 3: The General Chat
    def handle_general(self, state: AgentState):
        print("--- 💬 Entering General Chat Node ---")
        last_message = state["messages"][-1].content
        response = self.llm.invoke(
            f"You are a helpful assistant. Reply to: {last_message}"
        )
        return {"messages": [response]}

    def compile(self):
        # 1. Initialize the Graph with our State structure
        workflow = StateGraph(
            state_schema=AgentState,
            input_schema=AgentInput,
        )

        # 2. Add the Nodes
        workflow.add_node("categorizer", self.categorize_input)
        workflow.add_node("math_node", self.handle_math)
        workflow.add_node("general_node", self.handle_general)

        # 3. Set the Entry Point
        # When the graph starts, the first person to touch the ball is the
        # 'categorizer'
        workflow.set_entry_point("categorizer")

        # 4. Add Conditional Edges
        # After 'categorizer' runs, look at 'routing_logic' to decide where
        # to go next.
        workflow.add_conditional_edges(
            # From this node...
            "categorizer",
            # ...run this logic...
            self.routing_logic,
            {
                # ...and map the output to a node.
                "math_node": "math_node",
                "general_node": "general_node",
            },
        )

        # 5. Add Normal Edges
        # After math or general chat, we are done. Go to END.
        workflow.add_edge("math_node", END)
        workflow.add_edge("general_node", END)

        # 6. Compile
        return workflow.compile()


def print_ai_messages(msgs: list[AIMessage]):
    for i in msgs:
        print(f"id: {i.id}")
        print(f"content: {i.content}")
        print(50 * "-")


def main():
    """Run main function."""
    obj = AgentTest()
    app = obj.compile()

    # Test 1: A Math Question
    print("\n--- TEST 1: Math ---")
    inputs_1: AgentInput = {
        "messages": [
            HumanMessage(
                content="What is 55 multiplied by 10?",
            ),
        ],
    }

    # Stream the output to see the steps
    for event in app.stream(inputs_1):
        for key, value in event.items():
            print(f"Finished running: {key}")
            print_ai_messages(value.get("messages", []))

    # Test 2: A Casual Greeting
    print("\n--- TEST 2: General ---")
    inputs_2: AgentInput = {
        "messages": [
            HumanMessage(
                content="Tell me a fun fact about history.",
            ),
        ],
    }

    for event in app.stream(inputs_2):
        for key, value in event.items():
            print(f"Finished running: {key}")
            print_ai_messages(value.get("messages", []))


if __name__ == "__main__":
    main()
