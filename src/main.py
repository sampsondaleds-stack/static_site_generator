import os
import shutil
from block import markdown_to_html_node
from extractmarkdown import extract_title
from pathlib import Path
import sys


def main():
    basepath = "/"
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    source = "static"
    destination = "docs"
    from_path = "content"
    template_path = "template.html"
    dest_path = "docs"
    if os.path.exists(destination):
        shutil.rmtree(destination)
        print("deleting destination folder")
    copy_contents(source, destination)
    generate_pages_recursive(from_path, template_path, dest_path, basepath)

       
def copy_contents(source, destination):
    directories = os.listdir(source)
    if not os.path.exists(destination):
        os.mkdir(destination)
        print(f"creating destination folder {destination}")
    for file in directories:
        if os.path.isfile(os.path.join(source, file)):
            shutil.copy(os.path.join(source, file), destination)
            print(f"copy {file}, to {destination}")
        else:
            copy_contents(os.path.join(source, file), os.path.join(destination, file))

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    directories = os.listdir(dir_path_content)
    for file in directories:
        from_path = os.path.join(dir_path_content, file)
        dest_path = os.path.join(dest_dir_path, file)        
        if os.path.isfile(from_path):
            dest_path = Path(dest_path).with_suffix(".html")
            generate_page(
                from_path, 
                template_path, 
                dest_path,
                basepath
                )
        else:
            generate_pages_recursive(
                from_path, 
                template_path, 
                dest_path,
                basepath
            )

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    #save the contents of the markdown file
    with open(from_path, "r") as file:
        text = file.read()
    #save the contents of the template file
    with open(template_path, "r") as file:
        template = file.read()
    #create the html content
    html_string = markdown_to_html_node(text).to_html()
    title = extract_title(text)
    #update the template with the content extracted above
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html_string)
    template = template.replace('href="/', f'href="{basepath}')
    template = template.replace('src="/', f'src="{basepath}')
    #create the destination directories if they don't already exist
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    #write the updated template to the destination file
    with open(dest_path, "w") as file:
        file.write(template)

main()
