import os
import subprocess
import sys


__all__ = ['PyProject']


class PyProject:
    def __init__(self, name, git=False, git_hub=False, module=False):
        path, name = os.path.split(name)
        if path.startswith('~'):
            self._path = os.path.expanduser(path)
        else:
            self._path = os.path.abspath(path)
        self._name = name
        self._full_path = os.sep.join((self._path, self._name))
        
        self._git_hub = git_hub
        self._git = git_hub if git_hub else git
        
        self._is_module = module

        self._git_ignore = [
            '**/.*.swp',
            '**/*.pyc',
            '**/__pycache__',
            '/config.py']
    
    def create(self):
        os.mkdir(self._full_path)
        self._setup_module()
        self._setup_git()
        self._create_base_files()
    
    def _setup_module(self):
        if self._is_module:
            self._touch_file('__init__.py')
    
    def _setup_git(self):
        if self._git:
            self._create_git_ignore()
            self._init_git()

            if self._git_hub:
                pass
        
    def _create_git_ignore(self):
        ignore_file = self._get_rel_file_path('.gitignore')
        with open(ignore_file, 'w') as out:
            out.writelines('\n'.join(self._git_ignore))
    
    def _init_git(self):
        last_dir = os.curdir
        os.chdir(self._full_path)
        subprocess.run('git init .', check=True, shell=True)
        os.chdir(last_dir)
    
    def _create_base_files(self):
        self._touch_file('config.py')
        main = self._get_rel_file_path('main.py')
        with open(main, 'w') as out:
            out.write('#!/usr/bin/env python3\n\n\ndef main():\n    pass')
            out.write('\n\n\nif __name__ == "__main__":\n    main()\n')
    
    def _get_rel_file_path(self, path):
        return os.sep.join((self._full_path, path))
    
    def _touch_file(self, path):
        rel_path = self._get_rel_file_path(path)
        with open(rel_path, 'a'):
            os.utime(rel_path, None)