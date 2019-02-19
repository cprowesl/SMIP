
class Lesson:

    """
    Creates a lesson instance
    prompt: String that describes what to do in this lesson
    answer: Dict that stores the necessary registers as keys
        and the correct final values as their value mapping
    """
    def __init__(self, prompt, answer):
        self.lesson_prompt = prompt
        self.lesson_answer = {}
        pass

    """
    Checks if the solution provided is correct for this lesson
    solution: Dict containing register value mappings to be checked 
        against this lesson's answer
    
    :returns True if solution is correct, False otherwise
    """
    def check_solution(self, solution):
        for answer_register, answer_value in self.lesson_answer.items():
            if answer_value != solution.get(answer_register, None):
                return False

        return True