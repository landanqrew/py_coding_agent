import unittest
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file

class Tests(unittest.TestCase):
    '''def __init__(self):
        super().__init__()'''

    def test_get_files_info(self):
        # valid case
        file_info = get_files_info("calculator", "pkg")
        # print(file_info)
        self.assertEqual("file_size" in file_info, True)
        self.assertEqual("is_dir" in file_info, True)

        # should work with the current directory
        file_info = get_files_info("calculator", ".")
        # print(file_info)
        self.assertEqual("file_size" in file_info, True)
        self.assertEqual("is_dir" in file_info, True)


        # should raise ValueError if the directory is outside the working directory
        self.assertRaises(ValueError, get_files_info, "calculator", "/bin")

        # should raise ValueError if the directory is not a directory
        self.assertRaises(ValueError, get_files_info, "calculator", "pkg/calculator.py")

        # should raise ValueError if the directory is not a subdirectory of the working directory
        self.assertRaises(ValueError, get_files_info, "calculator", "../")

        '''try: 
            get_files_info("calculator", "pkg/calculator.py")
        except ValueError as e:
            print(e)'''

    def test_get_file_content(self):
        # valid case
        file_content = get_file_content("calculator", "pkg/calculator.py")
        # print(file_content)
        self.assertEqual(len(file_content) > 0, True)

        # valid case
        file_content = get_file_content("calculator", "main.py")
        # print(file_content)
        self.assertEqual(len(file_content) > 0, True)

        # valid case
        file_content = get_file_content("calculator", "lorem.txt")
        # print(f"test_get_file_content: LEN: {len(file_content)}")
        self.assertEqual(len(file_content) > 0, True)

        # should raise ValueError if the file is outside the working directory
        self.assertRaises(ValueError, get_file_content, "calculator", "/bin/cat")

        # should raise ValueError if the file is not a file
        self.assertRaises(ValueError, get_file_content, "calculator", "pkg")

        try:
            get_file_content("calculator", "/bin/cat")
        except ValueError as e:
            print(e)
        except Exception as e:
            print(e)

    def test_write_file(self):
        # valid case
        output = write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
        print(output)
        with open("calculator/lorem.txt", "r") as f:
            file_contents = f.read()
        print(file_contents)
        self.assertEqual(file_contents, "wait, this isn't lorem ipsum")

        output = write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
        print(output)
        with open("calculator/pkg/morelorem.txt", "r") as f:
            file_contents = f.read()
        print(file_contents)
        self.assertEqual(file_contents, "lorem ipsum dolor sit amet")

        # should raise ValueError if the file is outside the working directory
        self.assertRaises(ValueError, write_file, "calculator", "/tmp/temp.txt", "this should not be allowed")

        # should raise ValueError if the file is a directory
        self.assertRaises(ValueError, write_file, "calculator", "pkg", "this should not be allowed")
        
        

if __name__ == "__main__":
    unittest.main()
    


        
        
