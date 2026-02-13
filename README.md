# Code Generation Tool

This project implements a code generator that parses a draw.io XML model and generates corresponding code in **Java**. It is designed to handle complex relationships, inheritance, composition and multiplicity.

## Code Quality
<<TO BE ADDED HERE>>

## What it does:

- **Multi Language Support**: Generates both Java classes from a single XML model.
- **Complex Model Handling**: Supports entities, relationships (1 to 1, 1 to many), and inheritance.
  
## Modeling Rules (Draw.io)

For the generator to work correctly with your own draw.io models:
- **Entities**: Use Rectangles. The label inside is the Class Name.
- **Relationships**:
    - **Composition/List**: Use Arrows labeled with `(N)` (e.g., `has (N)`). This generates a `List<Type>`.
    - **Single Field**: Use Arrows with a simple label (e.g., `has`).
    - **Inheritance**: Use an arrow with `End Arrow = Block` and `Fill = None` (Hollow Triangle).
        - **Direction**: Point from **Child** to **Parent**.
        - Example: `Student -> Person` means `Student extends Person`.
        - The generator strictly enforces this style.

## Usage

### 1. Generate Code

Run the generator by providing the path to the XML model and the desired output directory.

**Syntax:**

```bash
python3 generator.py --model <path_to_xml> --output <output_directory>
```

**Example:**

```bash
python3 generator.py --model examples/example2/model/diagram.xml --output examples/example2/src-gen
```

[![SonarQube Cloud](https://sonarcloud.io/images/project_badges/sonarcloud-light.svg)](https://sonarcloud.io/summary/new_code?id=Nadeem-Mohamed_2AA4-code-gen-bonus-2)

### Generated Output

The tool will create one subdirectory in the output folder:
- `java/`: Contains the generated `.java` files.
