#!/usr/bin/python3
"""
MIT License

Copyright 2023 Ananthanarayanan Venkitakrishnan

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

"""
Homepage: https://github.com/ananthvk/codeforces-solutions
The purpose of this tool is to speedily and quickly generate source files with the ability to compile and execute them using
the cli for online competitive programming contests.
Currently this tool only supports codeforces(https://codeforces.com)
"""

import pathlib
import re
import sys
import json
import typing
import shutil
import textwrap
import os
from bs4 import BeautifulSoup
import requests
import subprocess

file_safe = re.compile("[0-9a-zA-Z_]")  # 0 to 9, a to z and A to Z
not_file_safe = re.compile("[^0-9a-zA-Z_]")  # 0 to 9, a to z and A to Z
REQUEST_TIMEOUT = 30  # Number of seconds after which a HTTP requests times out


def get_problem_json(info: typing.Dict):
    return {
        "source_file": info["filename"] + ".cpp",
        "output_file": info["filename"] + ".bin",
        "lang": "C++",
        "command": "/usr/bin/clang++",
        "args": [
            "-W",
            "-Wall",
            "-Wextra",
            "-pedantic",
            "-gdwarf-4",
            "-O0",
            "-fsanitize=integer,address,undefined,integer-divide-by-zero,shift,null,return,signed-integer-overflow,float-divide-by-zero,float-cast-overflow,bounds,alignment,vptr,leak",
            "-pedantic",
            "-Wno-sign-conversion",
            "-Wno-sign-compare",
            "-ftrapv",
        ],
        "info": info,
    }

def get_solution_path(contest_id, problem_index):
    return pathlib.Path('codeforces') / pathlib.Path(f'{contest_id}{problem_index}')

class Action:
    def __init__(self) -> None:
        pass

    def execute(self) -> None:
        pass


class CreateFileAction(Action):
    def __init__(self, path: pathlib.Path | str, overwrite=False) -> None:
        super().__init__()
        if isinstance(path, str):
            self.path = pathlib.Path(path)
        elif isinstance(path, pathlib.Path):
            self.path = path
        else:
            raise TypeError(
                "Expected a string or a pathlib.Path object to represent a path, received a ",
                type(self.path),
            )
        self.overwrite = overwrite

    def execute(self) -> None:
        # If the file exists and overwrite is false, do nothing
        if os.path.exists(self.path) and not self.overwrite:
            return

        # Create the necessary directories
        try:
            self.path.resolve().parent.mkdir(parents=True, exist_ok=True)
        except NotADirectoryError:
            raise RuntimeError(
                "ERROR: Could not create folders/files since it already exists"
            )

        # Create the emtpy file
        with open(self.path, "w"):
            pass


class CreateFolderAction(Action):
    def __init__(self, path: pathlib.Path | str) -> None:
        super().__init__()
        if isinstance(path, str):
            self.path = pathlib.Path(path)
        elif isinstance(path, pathlib.Path):
            self.path = path
        else:
            raise TypeError(
                f"Expected a string or a pathlib.Path object to represent a path, received a {type(path)}"
            )

    def execute(self) -> None:
        # Create the necessary directories
        self.path.resolve().mkdir(parents=True, exist_ok=True)


class CopyFileContentAction(Action):
    def __init__(
        self,
        from_path: pathlib.Path | str,
        to_path: pathlib.Path | str,
        overwrite=False,
    ) -> None:
        super().__init__()
        if isinstance(from_path, str):
            self.from_path = pathlib.Path(from_path)
        elif isinstance(from_path, pathlib.Path):
            self.from_path = from_path
        else:
            raise TypeError(
                f"Expected a string or a pathlib.Path object to represent from a path, received a {type(from_path)}"
            )

        if isinstance(to_path, str):
            self.to_path = pathlib.Path(to_path)
        elif isinstance(to_path, pathlib.Path):
            self.to_path = to_path
        else:
            raise TypeError(
                f"Expected a string or a pathlib.Path object to represent a to path, received a {type(to_path)}"
            )

        self.overwrite = overwrite

    def execute(self) -> None:
        if not os.path.exists(self.from_path):
            raise ValueError(f"{self.from_path} does not exist")
        if os.path.exists(self.to_path) and not self.overwrite:
            raise ValueError(
                "ERROR: Could not copy file contents since the file already exists"
            )

        CreateFolderAction(self.to_path).execute()
        shutil.copy(self.from_path, self.to_path)


class CodeforcesProblemParser:
    """
    A class for parsing codeforces problem statements
    This makes use of the convenient class attributes in div to extract the required information.
    So this parser can break if the site is updated.
    """

    def __init__(self) -> None:
        pass

    def from_html(self, path: str | pathlib.Path) -> typing.Dict:
        with open(path, "rb") as fil:
            return self.from_content(fil.read())

    def from_content(self, html_content: str | bytes) -> typing.Dict:
        problem_info = {
            "url": "",
            "name": "",
            "filename": "",
            "id": "",
            "index": "",
            "problem_statement": [],
            "input": [],
            "output": [],
            "tests": [],
            "notes": [],
        }
        soup = BeautifulSoup(html_content, features="html.parser")
        try:
            problem = soup.select(".problem-statement")[0]
        except:
            pass

        try:
            div = problem.findAll(attrs={"class": None})[0]
            problem_info["problem_statement"] = [i.get_text() for i in div.findAll("p")]
        except:
            pass

        try:
            div = problem.select(".input-specification")[0]
            problem_info["input"] = [i.get_text() for i in div.findAll("p")]
        except:
            pass

        try:
            div = problem.select(".output-specification")[0]
            problem_info["output"] = [i.get_text() for i in div.findAll("p")]
        except:
            pass

        try:
            div = problem.select(".sample-tests")[0]
            problem_info["tests"] = [i.get_text(separator="\n") for i in div]
        except:
            pass

        try:
            div = problem.select(".note")
            if div is not None:
                problem_info["notes"] = [i.get_text() for i in div]
        except:
            pass

        try:
            problem_url = soup.select(
                "#pageContent > div.second-level-menu > ul > li.current.selectedLava > a"
            )[0]

            contest_id = [i for i in problem_url.attrs["href"].split("/") if i.strip()][
                -1
            ]
            problem_info["id"] = contest_id

            title_string = problem.find("div", {"class": "title"}).text
            contents = [i for i in title_string.split(".")]
            problem_info["index"] = contents[0].strip()

            file_name = "".join(contents[1:])
            file_prefix = f'{problem_info["id"]}{problem_info["index"]}_'
            problem_info["filename"] = re.sub(not_file_safe, "", file_prefix) + re.sub(
                not_file_safe, "", file_name
            )

            contents = [i.strip() for i in contents]
            problem_info["name"] = " ".join(contents[1:]).strip()

            problem_info[
                "url"
            ] = f'https://codeforces.com{problem_url["href"]}/problem/{problem_info["index"]}'
        except:
            pass

        return problem_info


class ProblemMeta:
    def __init__(self) -> None:
        pass

    def read(self, ob: str | pathlib.Path | typing.BinaryIO) -> typing.Dict:
        content = None
        if isinstance(ob, str) or isinstance(ob, pathlib.Path):
            with open(ob, "rb") as ipfile:
                content = ipfile.read()
        else:
            try:
                content = ob.read()
            except:
                raise AttributeError(
                    "Object does not contain read() method, file-like object expected"
                )

        return json.loads(content)


"""
Hacky hardcoded solution to make it work first
"""


def codeforces_generator(contest_id, problem_index):

    url = f"https://codeforces.com/contest/{contest_id}/problem/{problem_index}"

    solution_path = get_solution_path(contest_id, problem_index)
    CreateFolderAction(solution_path).execute()
    os.chdir(solution_path)

    if os.path.exists("problem.json"):
        print(
            "problem.json already exists, delete problem.json to create a new project"
        )
        return

    try:
        req = requests.get(
            url, headers={"User-Agent": "cptool.py"}, timeout=REQUEST_TIMEOUT
        )
    except Exception as e:
        print(f"ERROR: Could not get problem info from {url}")
        return

    if req.status_code != requests.codes.ok:
        print(f"ERROR: {req.status_code} while getting info from server")
        return

    parser = CodeforcesProblemParser()
    info = parser.from_content(req.content)
    problem_json = get_problem_json(info)

    # Create the required files if it does not exist
    actions = [
        CreateFileAction(problem_json["source_file"]),
        CreateFileAction("problem.json"),
    ]
    for action in actions:
        action.execute()

    with open("problem.json", "w") as prob_json:
        json.dump(problem_json, prob_json, sort_keys=True, indent=4)


def codeforces_build() -> int:
    if not os.path.exists("problem.json"):
        print(
            "ERROR: problem.json does not exist, please create problem.json using python cptool.py cfgen <contest id> <problem index>"
        )
        return 1

    parser = ProblemMeta()
    problem_json = parser.read("problem.json")

    # TODO: Add error checking if the keys are not present in the json file
    args = []
    args += [problem_json["command"]]
    args += problem_json["args"]
    args += [problem_json["source_file"]]
    args += ["-o"]
    args += [problem_json["output_file"]]

    # print(' '.join(args), file=sys.stderr)
    print(f'Compiling {problem_json["source_file"]}...', file=sys.stderr)

    exit_code = subprocess.run(
        args,
        shell=False,
    ).returncode
    if exit_code != 0:
        print("ERROR: Build failed")
        return 1

    return 0


def codeforces_execute():
    if not os.path.exists("problem.json"):
        print(
            "ERROR: problem.json does not exist, please create problem.json using python cptool.py cfgen <contest id> <problem index>"
        )
        return
    if codeforces_build() != 0:
        print("ERROR: Not executing since build failed")
        return

    parser = ProblemMeta()
    problem_json = parser.read("problem.json")

    op_exe = f'./{problem_json["output_file"]}'

    print(f"Executing {op_exe[2:]} ...", file=sys.stderr)

    exit_code = subprocess.run([op_exe], shell=False)


def usage_help():
    print("Usage: python cptool.py [options]")
    print("Arguments")
    print("help                               Prints this help message and exits")
    print(
        "build                              Compiles the source file, but does not run it"
    )
    print("execute                            Compiles the source file and executes it")
    print("quick                              Generates a quick problem project")
    print(
        "cfgen <contest id> <problem index> Downloads the project information from codeforces.com and creates the problem.json"
    )


def main():
    if len(sys.argv) == 2:
        match sys.argv[1]:
            case "help":
                usage_help()
            case "quick":
                raise NotImplementedError()
            case "build":
                codeforces_build()
            case "execute":
                codeforces_execute()
            case default:
                usage_help()

    elif len(sys.argv) == 4:
        match sys.argv[1]:
            case "cfgen":
                codeforces_generator(sys.argv[2], sys.argv[3])
            case default:
                usage_help()
        pass
    else:
        usage_help()


if __name__ == "__main__":
    main()
