# scaffold

A CLI tool to setup developer environment hosted on Docker locally.

scaffold is an open-source command-line tool designed to quickly set up developer environments using Docker. It allows developers to create new projects with pre-configured environments for various project types (e.g., Node.js, Python, FastAPI, Django) with just a few simple commands.

## Features

- Easy-to-use CLI interface
- Supports multiple project types
- Automatically creates a Docker container for your project
- Opens Visual Studio Code connected to the Docker container
- Remembers your last used project directory

## Installation

You can install Scaffold directly from PyPI:

```bash
pip install scaffold-dev
```

This will install the `scaffold` command and make it available in your PATH.

## Prerequisites

- Python 3.6+
- Docker
- Visual Studio Code with Remote - Containers extension

## Usage

You can use Scaffold in two ways:

### Interactive Mode

Run the command without any arguments to enter interactive mode:

```bash
scaffold
```

You'll be prompted to enter:

- Project directory (or press Enter to use the last used directory)
- Project type (e.g., node, python, fastapi, django)
- Project name

### Command-line Arguments

You can also provide all necessary information as command-line arguments:

```bash
scaffold --directory /path/to/projects --type node --name my-new-project
```

## Contributing

We welcome contributions to Scaffold! Here's how you can help:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Write your code and tests.
4. Ensure all tests pass.
5. Submit a pull request with a clear description of your changes.

### Adding New Project Types

To add support for a new project type:

1. Create a new directory under `scaffold/templates/` with the name of your project type.
2. Add a `Dockerfile` to this new directory, configured for the new project type.
3. Test the new project type thoroughly.
4. Update the documentation to include the new project type.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

If you have any questions or feedback, please open an issue on this GitHub repository.

Thank you for using or contributing to Scaffold!
