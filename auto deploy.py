import os
import subprocess
import json

def run_command(command):
    """ Run a shell command and capture the output. """
    try:
        print(f"Running command: {command}")
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return result.stdout.decode("utf-8")
    except subprocess.CalledProcessError as e:
        print(f"Error executing command '{command}': {e.stderr.decode('utf-8')}")
        exit(1)

def install_gh_pages():
    """ Install gh-pages via npm. """
    print("Installing gh-pages package via npm...")
    run_command("npm install gh-pages --save-dev")

def update_package_json(project_name):
    """ Update the package.json with homepage and deployment scripts. """
    print("Updating package.json...")

    # Load the existing package.json
    package_json_path = "package.json"
    with open(package_json_path, "r") as f:
        package_data = json.load(f)

    # Update the homepage and scripts
    homepage_url = f"https://{project_name}.github.io"
    package_data["homepage"] = homepage_url
    package_data["scripts"]["predeploy"] = "npm run build"
    package_data["scripts"]["deploy"] = "gh-pages -d build"

    # Write the modified package.json back to file
    with open(package_json_path, "w") as f:
        json.dump(package_data, f, indent=2)

    print(f"Updated package.json with homepage: {homepage_url}")

def initialize_git_repo(project_name):
    """ Initialize a git repo, add remote and make the initial commit. """
    if not os.path.isdir(".git"):
        print("Initializing Git repository...")
        run_command("git init")
    
    # Get the current project folder name (which will be used as the GitHub repo name)
    repo_name = project_name

    # Check if the remote 'origin' already exists
    try:
        remotes = run_command("git remote").strip()
        if 'origin' not in remotes:
            print("Adding remote 'origin'...")
            remote_url = f"git@github.com:ziadMhCs/{repo_name}.git"
            run_command(f"git remote add origin {remote_url}")
        else:
            print("Remote 'origin' already exists. Skipping remote addition.")
    except Exception as e:
        print(f"Error checking remote: {e}")
        exit(1)

    # Stage and commit the changes
    print("Staging and committing initial files to git...")
    run_command("git add .")
    run_command('git commit -m "Initial commit"')

def git_sync():
    """ Sync local repository with GitHub (push changes). """
    print("Syncing with remote GitHub repository...")

    # Check if the current branch is 'main', if not, create it
    current_branch = run_command("git rev-parse --abbrev-ref HEAD").strip()
    if current_branch != "main":
        print("No 'main' branch found, creating it...")
        run_command("git checkout -b main")

    # Now, push the code to the remote 'main' branch
    run_command("git push -u origin main")

def main():
    # Get the current folder name to match the GitHub repo
    project_folder = os.path.basename(os.getcwd())

    print(f"Setting up React project for GitHub Pages deployment: {project_folder}")

    # Install gh-pages and update package.json
    install_gh_pages()

    # Update package.json to configure homepage and deploy scripts
    update_package_json(project_folder)

    # Initialize git repository and set remote
    initialize_git_repo(project_folder)

    # Push the local repository to GitHub
    git_sync()

    print("React project is now set up and deployed to GitHub Pages!")

if __name__ == "__main__":
    main()
