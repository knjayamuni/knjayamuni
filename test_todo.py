import unittest
from unittest.mock import patch, mock_open, call
import todo # Your main application file
import os

class TestTodoApp(unittest.TestCase):

    def setUp(self):
        # Point to a test-specific tasks file
        self.test_tasks_file = "test_tasks.txt"
        todo.TASKS_FILE = self.test_tasks_file
        # Ensure the test tasks file is clean before each test
        if os.path.exists(self.test_tasks_file):
            os.remove(self.test_tasks_file)

    def tearDown(self):
        # Clean up the test tasks file after each test
        if os.path.exists(self.test_tasks_file):
            os.remove(self.test_tasks_file)
        # Reset to default tasks file
        todo.TASKS_FILE = "tasks.txt"

    def test_load_tasks_file_not_found(self):
        """Ensure load_tasks returns an empty list if the tasks file doesn't exist."""
        # Make sure the file does not exist for this specific test
        if os.path.exists(self.test_tasks_file):
            os.remove(self.test_tasks_file)
        self.assertEqual(todo.load_tasks(), [])

    def test_save_and_load_tasks(self):
        """Save a few sample tasks and load them back."""
        tasks_to_save = ["Task 1", "Task 2", "Another Task"]
        todo.save_tasks(tasks_to_save)
        loaded_tasks = todo.load_tasks()
        self.assertEqual(loaded_tasks, tasks_to_save)

    @patch('builtins.print')
    def test_add_task(self, mock_print):
        """Add a task and check if it's saved and confirmation is printed."""
        todo.add_task("New Task")
        loaded_tasks = todo.load_tasks()
        self.assertIn("New Task", loaded_tasks)
        mock_print.assert_called_with("Task added.")

    @patch('builtins.print')
    def test_view_tasks_empty(self, mock_print):
        """Test viewing tasks when the list is empty."""
        todo.view_tasks()
        mock_print.assert_called_with("No tasks in the list.")

    @patch('builtins.print')
    def test_view_tasks_with_items(self, mock_print):
        """Test viewing tasks when there are items in the list."""
        tasks_to_view = ["Task A", "Task B"]
        todo.save_tasks(tasks_to_view)
        todo.view_tasks()
        expected_calls = [
            call("1. Task A"),
            call("2. Task B")
        ]
        mock_print.assert_has_calls(expected_calls)

    @patch('builtins.print')
    def test_update_task_valid(self, mock_print):
        """Test updating an existing task with a valid index."""
        initial_tasks = ["Old Task"]
        todo.save_tasks(initial_tasks)
        todo.update_task(1, "Updated Task")
        loaded_tasks = todo.load_tasks()
        self.assertEqual(loaded_tasks, ["Updated Task"])
        mock_print.assert_called_with("Task updated.")

    @patch('builtins.print')
    def test_update_task_invalid_index(self, mock_print):
        """Test updating a task with an invalid (out of bounds) index."""
        initial_tasks = ["Task One"]
        todo.save_tasks(initial_tasks)
        todo.update_task(2, "This should not apply") # Index 2 for a 1-item list
        loaded_tasks = todo.load_tasks()
        self.assertEqual(loaded_tasks, initial_tasks) # Should be unchanged
        mock_print.assert_called_with("Error: Invalid task number.")

    @patch('builtins.print')
    def test_update_task_invalid_index_zero(self, mock_print):
        """Test updating a task with index 0 (invalid)."""
        initial_tasks = ["Task One"]
        todo.save_tasks(initial_tasks)
        todo.update_task(0, "This should not apply")
        loaded_tasks = todo.load_tasks()
        self.assertEqual(loaded_tasks, initial_tasks)
        mock_print.assert_called_with("Error: Invalid task number.")

    @patch('builtins.print')
    def test_mark_task_done_valid(self, mock_print):
        """Test marking a task as done with a valid index."""
        initial_tasks = ["Do Laundry"]
        todo.save_tasks(initial_tasks)
        todo.mark_task_done(1)
        loaded_tasks = todo.load_tasks()
        self.assertEqual(loaded_tasks, ["[DONE] Do Laundry"])
        mock_print.assert_called_with("Task marked as done.")

    @patch('builtins.print')
    def test_mark_task_done_already_done(self, mock_print):
        """Test marking a task that is already done."""
        initial_tasks = ["[DONE] Already Done Task"]
        todo.save_tasks(initial_tasks)
        todo.mark_task_done(1)
        loaded_tasks = todo.load_tasks()
        self.assertEqual(loaded_tasks, ["[DONE] Already Done Task"]) # Should be unchanged
        mock_print.assert_called_with("Task is already marked as done.")

    @patch('builtins.print')
    def test_mark_task_done_invalid_index(self, mock_print):
        """Test marking a task as done with an invalid index."""
        initial_tasks = ["A Task"]
        todo.save_tasks(initial_tasks)
        todo.mark_task_done(5) # Invalid index
        loaded_tasks = todo.load_tasks()
        self.assertEqual(loaded_tasks, initial_tasks) # Should be unchanged
        mock_print.assert_called_with("Error: Invalid task number.")

    @patch('builtins.print')
    def test_delete_task_valid(self, mock_print):
        """Test deleting a task with a valid index."""
        initial_tasks = ["Task X", "Task Y", "Task Z"]
        todo.save_tasks(initial_tasks)
        todo.delete_task(2) # Delete "Task Y"
        loaded_tasks = todo.load_tasks()
        self.assertEqual(loaded_tasks, ["Task X", "Task Z"])
        mock_print.assert_called_with("Task deleted.")

    @patch('builtins.print')
    def test_delete_task_invalid_index(self, mock_print):
        """Test deleting a task with an invalid index."""
        initial_tasks = ["Only Task"]
        todo.save_tasks(initial_tasks)
        todo.delete_task(3) # Invalid index
        loaded_tasks = todo.load_tasks()
        self.assertEqual(loaded_tasks, initial_tasks) # Should be unchanged
        mock_print.assert_called_with("Error: Invalid task number.")

    @patch('builtins.print')
    def test_load_tasks_io_error(self, mock_print):
        """Test load_tasks with an IOError/OSError during read."""
        # Make original todo.TASKS_FILE point to something that will cause an error
        # For this test, we mock load_tasks at a higher level to simulate file read error
        # directly, rather than trying to create a problematic file state.
        # The previous modification to todo.py already added IOError/OSError handling.
        # Here we ensure that if load_tasks itself raises it (e.g. due to mocked open failing)
        # or if the open inside load_tasks fails, the print occurs.

        # We need to test the behavior of functions *calling* load_tasks when load_tasks
        # itself indicates an error. Let's test view_tasks.
        # If load_tasks prints an error and returns [], view_tasks should print "No tasks..."

        # This test is slightly different from the subtask description,
        # as directly testing the print within load_tasks requires deeper mocking of 'open'.
        # Instead, we confirm that functions calling load_tasks behave as expected
        # when load_tasks returns an empty list due to an error.

        # Scenario: load_tasks encounters an error and prints its own message.
        # We'll mock `open` within `load_tasks` to simulate this.

        # Ensure the test file exists initially for `open` to be called
        with open(self.test_tasks_file, 'w') as f:
            f.write("some data\n")

        with patch('builtins.open', mock_open()) as mocked_file:
            mocked_file.side_effect = IOError("Simulated read error")
            # Call a function that uses load_tasks
            result = todo.load_tasks() # Call load_tasks directly to check its output and print
            self.assertEqual(result, []) # Should return empty list
            # Check that load_tasks printed the error
            mock_print.assert_called_with(f"Error: Could not read tasks from {self.test_tasks_file}. Simulated read error")

    @patch('builtins.print')
    @patch('builtins.open', new_callable=mock_open)
    def test_save_tasks_io_error(self, mock_file_open, mock_print):
        """Test save_tasks with an IOError/OSError during write."""
        # Configure the mock_open to raise IOError on write
        mock_file_open.side_effect = IOError("Simulated write error")

        tasks_to_save = ["Task 1"]
        todo.save_tasks(tasks_to_save) # Attempt to save tasks

        # Assert that the error message was printed
        mock_print.assert_called_with(f"Error: Could not save tasks to {self.test_tasks_file}. Simulated write error")
        # Ensure the file mock was indeed called (attempted to be opened for writing)
        mock_file_open.assert_called_once_with(self.test_tasks_file, "w")


if __name__ == '__main__':
    unittest.main()
