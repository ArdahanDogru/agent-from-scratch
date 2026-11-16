import anthropic
from dotenv import load_dotenv
from rich.console import Console
from rich.markdown import Markdown

load_dotenv()

client = anthropic.Anthropic()
console = Console() 

def calculator(operation, a, b):
	if operation == "*":
		return a * b
	elif operation == "-":
		return a - b
	elif operation == "+":
		return a + b
	elif operation == "/":
		return a / b

tools = [
{
    "name": "calculator",
    "description": "takes two numeric inputs, represented by variables a and b, and returns the result of the mathematical opration done with them. Operations can be multiplication, division, addition, and subtraction. Use this tool for any arithmetic operation instead of calculating yourself.",       # what it does and when to use it
    "input_schema": {
        "type": "object",
        "properties": {
		"operation": {
			"type": "string",
			"enum": ["+", "-", "*", "/"],
			"description": "the type of mathematical operations to be applied between a and b, the numeric values."
		},

		"a":{
			"type": "number",
			"description": "the first numeric value for which with the operation along with the second numeric value will be applied to."
		},

		"b":{
			"type": "number",
			"description": "the second numeric value that is applied to the first numeric value with the operation."
		}
	},
        "required": [ "operation", "a", "b"]
    },
}
]


messages = []
while True: 
	userMsg = input(">")
	if userMsg.lower() == 'quit':
		print("Exiting the loop. Goodbye!")
		break 

	messages.append({"role": "user", "content": userMsg})

	while True:
		response = client.messages.create(
			model="claude-haiku-5-5",
			max_tokens=4000,
			tools=tools,
			messages=messages,
		)

		for block in response.content:
			if block.type == "text":
				console.print(Markdown(block.text))
			elif block.type == "tool_use":
				if block.name == "calculator":
					result = calculator(**block.input)
			elif block.type == "thinking":
				console.print(block.thinking, style="dim")
		messages.append({"role": "assistant", "content": response.content})

		if response.stop_reason != "tool_use":
			break

		tool_results = []
		for block in response.content:
			if block.type == "tool_use":
				result = calculator(**block.input)
				tool_results.append({
					"type": "tool_result",
					"tool_use_id": block.id,
					"content": str(result),
				})
		messages.append({"role": "user", "content": tool_results})
print(messages)

