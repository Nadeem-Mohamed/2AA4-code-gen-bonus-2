# Code Generation Tool

This project implements a code generator that parses a draw.io XML model and generates corresponding code in **Java** and **Python**. It is designed to handle complex relationships, inheritance, and flexible folder structures.

## Features

- **Multi-Language Support**: Generates both Java classes and Python classes from a single XML model.
- **Complex Model Handling**: Supports entities, relationships (1-to-1, 1-to-many), and inheritance ("is_a").
- **CLI Interface**: Easy-to-use command-line interface for generation.

## Project Structure

- `generator.py`: Main script to parse an XML model and generate code.
- `examples/`:
    - `default/`: Contains a simple university model and its generated code.
    - `new/`: Contains an expanded complex model (18+ entities) and its generated code.

## Usage

### 1. Generate Code

Run the generator by providing the path to the XML model and the desired output directory.

**Syntax:**

```bash
python3 generator.py --model <path_to_xml> --output <output_directory>
```

**Example 1: Generating from the Default Model**

```bash
python3 generator.py --model examples/default/model/diagram.xml --output examples/default/src-gen
```

**Example 2: Generating from the New Complex Model**

```bash
python3 generator.py --model examples/new/model/diagram.xml --output examples/new/src-gen
```

### Generated Output

The tool will create two subdirectories in the output folder:
- `java/`: Contains the generated `.java` files.
- `python/`: Contains the generated `.py` files.

## Modeling Rules (Draw.io)

For the generator to work correctly with your own draw.io models:
- **Entities**: Use Rectangles. The label inside is the Class Name.
- **Relationships**: Use Arrows.
    - **Label**: `<fieldName> (N)` for 1-to-many lists, or just `<fieldName>` for 1-to-1.
    - **Inheritance**: Use an arrow with an empty triangle head (Generalization) labeled `is_a`.
