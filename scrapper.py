import programmers
import wanted

def scrap(word):
    jobs = programmers.get_jobs(word.capitalize()) + wanted.get_jobs(word)
    return jobs