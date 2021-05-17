from typing import Dict, List, Tuple
from mod_ansible_autodoc.markdown.parse import (
    get_all_headings,
    parse_section,
    get_list_items,
    get_examples,
)


def format_todo(todo: str) -> str:
    """
    Format todo.

    Args:
        todo (str): todo section str

    Returns:
        (str) -> formatted todo
    """
    if not todo:
        return ""

    headings = get_all_headings(todo, 4)

    formatted_todo_content = []
    for heading in headings:
        # Get inner text
        section = parse_section(todo, heading, "#", 4, 4)
        section = section.strip()

        # Get TODO items
        todo_items = get_list_items(section)

        for todo_item in todo_items:
            # Format current item
            formatted_item = (
                f"* **{heading.replace(':', '')}:** "
                f"{todo_item.lstrip('*').strip('-').strip()}"
            )
            formatted_todo_content.append(formatted_item)

    return "\n".join(formatted_todo_content)


def format_actions(actions: str) -> str:
    """
    Format actions.

    Args:
        actions (str): actions section str

    Returns:
        (str) -> formatted actions
    """
    if not actions:
        return ""

    headings = get_all_headings(actions, 4)

    hashes_str = "#" * 4 + " "
    formatted_actions_content = []
    for heading in headings:
        # Get inner text
        section = parse_section(actions, heading, "#", 4, 4)
        section = section.strip()

        # Ensure capitalization
        section_lines = section.split("\n")
        fheading = hashes_str + section_lines[0].replace(hashes_str, "")
        section_lines[0] = fheading
        section = "\n".join(section_lines)

        formatted_actions_content.append(section)

    return "\n".join(formatted_actions_content)


def format_tags(tags: str) -> str:
    """
    Format tags. For now, uses the same formatting as "format_actions".

    Args:
        tags (str): tags section str

    Return:
        (str) -> formatted tags
    """
    return format_actions(tags)


def format_variables(variables: str) -> Tuple[Dict[str, List[List[str]]], str]:
    """
    Format variables.

    Args:
        variables (str): variables section str

    Return:
        (Tuple[Dict[str, List[List[str]]], str]) -> variables json, example str
    """
    if not variables:
        return "", ""

    # Get variable items
    var_items = get_list_items(variables)

    # Get examples
    examples = get_examples(variables)

    # Format variables
    formatted_variables = [["Name", "Default Value", "Description"]]
    for var_item in var_items:
        # Get name
        var_item_data = var_item.split(":", 1)
        name = var_item_data[0].lstrip("*").strip().strip("`")

        # If name is "docker_edition", check if it has an example
        # ... if it does, add hyperlink
        for example in examples:
            if name in example:
                name = f"[{name}](#{name})"

        # Get value
        var_item_data = var_item_data[1].split("-")
        default_value = var_item_data[0].strip().strip("`")

        # Get description
        description = var_item_data[1].strip()

        # Append to the formatted variable list
        formatted_variables.append([name, default_value, description])

    variables_json = {"role_variables": formatted_variables}

    return variables_json, format_variable_examples(variables)


def format_variable_examples(variables: str) -> str:
    """
    Format variable examples.

    Args:
        variables (str): variables section str

    Return:
        (str): formatted examples
    """
    if not variables:
        return ""

    # Get examples
    examples = get_examples(variables)

    formatted_examples = []
    for example in examples:
        # Take out beginning ``yaml and ending ``
        if example.startswith("``yaml"):
            example = example.replace("``yaml", "")

        if example.endswith("``"):
            example = example[:-2]

        # Remove extra whitespace
        example = example.strip()

        # Extract name
        example_data = example.split(":", 1)
        name = example_data[0]

        # Extract items
        items = example_data[1].replace('"', "`")

        # Build heading
        head = f"#### {name}\n\n"

        formatted_examples.append(head + "```\n" + f"{name}:{items}" + "\n```")

    return "\n\n".join(formatted_examples)


def add_title(
    text: str, args: Dict[str, str], arg_name: str, default_title: str
) -> str:
    # If empty, dont add anything
    if not text:
        return text

    title = args.get(arg_name, default_title)

    if title.strip():
        return f"{title}\n{text}"

    return f"{default_title}\n{text}"
