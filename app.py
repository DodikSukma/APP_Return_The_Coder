# Import Pandas to read data
import pandas as pd
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

def fibonacci(n):
    """
    Calculate the nth Fibonacci number.

    Parameters:
        n (int): The position of the Fibonacci number to be calculated.

    Returns:
        int: The nth Fibonacci number.
    """
    if n <= 0:
        return -1
    elif n == 1 or n == 2:
        return 1
    else:
        fib_prev_prev = 1
        fib_prev = 1
        fib_current = 0
        for i in range(3, n + 1):
            fib_current = fib_prev + fib_prev_prev
            fib_prev_prev = fib_prev
            fib_prev = fib_current
        return fib_current

def sum_fibonacci(n):
    """
    Calculate the sum of the first n Fibonacci numbers.

    Parameters:
        n (int): The number of Fibonacci numbers to be summed.

    Returns:
        int: The sum of the first n Fibonacci numbers.
    """
    sum_fib = 0
    for i in range(1, n + 1):
        sum_fib += fibonacci(i)
    return sum_fib

death_data = []

@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Handle the main page.

    If the method is POST, calculate the count of death based on input data and redirect to the result page.
    If the method is GET, render the index.html template.
    """
    if request.method == 'POST':
        year_of_death = int(request.form['year_of_death'])
        age_of_death = int(request.form['age_of_death'])
        n = year_of_death - age_of_death

        sum_suku = sum_fibonacci(n)
        if n < 0:
            return "Death Data not found! The provided data is invalid. Please try again."

        death_data.append({'Year': n, 'Count Of Death': sum_suku})
        return redirect(url_for('result'))

    return render_template('index.html')

@app.route('/delete/<int:index>', methods=['POST'])
def delete_data(index):
    """
    Handle data deletion.

    Parameters:
        index (int): The index of the data to be deleted.

    Redirect to the result page after deleting the data.
    """
    if index >= 0 and index < len(death_data):
        del death_data[index]
    return redirect(url_for('result'))

@app.route('/result', methods=['GET', 'POST'])
def result():
    """
    Handle the result page.

    If the method is POST, redirect to the result page again.
    If the method is GET, calculate the average count of death and render the result.html template.
    """
    if request.method == 'POST':
        return redirect(url_for('result'))

    average = calculate_average(death_data)
    return render_template('result.html', data=death_data, average=average)

def calculate_average(data_list):
    """
    Calculate the average count of death.

    Parameters:
        data_list (list): A list of dictionaries containing the 'Count Of Death' for each data entry.

    Returns:
        float: The average count of death.
    """
    total_death = sum([data['Count Of Death'] for data in data_list])
    return total_death / len(data_list) if len(data_list) > 0 else 0

if __name__ == "__main__":
    app.run(debug=True)
