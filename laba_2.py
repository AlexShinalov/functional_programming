students = [
    {'name': 'Nikolay', 'age': 20, 'grades': [2, 5, 4, 3]},
    {'name': 'Anna', 'age': 22, 'grades': [4, 5, 3, 5]},
    {'name': 'John', 'age': 21, 'grades': [3, 4, 3, 2]},
    {'name': 'Maria', 'age': 19, 'grades': [5, 4, 5, 4]},
    {'name': 'Michael', 'age': 23, 'grades': [2, 3, 2, 4]},
    {'name': 'Olga', 'age': 20, 'grades': [4, 3, 5, 2]},
    {'name': 'David', 'age': 24, 'grades': [5, 4, 3, 4]},
    {'name': 'Elena', 'age': 21, 'grades': [2, 2, 3, 5]},
    {'name': 'Alex', 'age': 22, 'grades': [4, 4, 5, 3]},
    {'name': 'Sofia', 'age': 20, 'grades': [5, 5, 4, 4]},
    {'name': 'Robert', 'age': 23, 'grades': [3, 3, 4, 2]},
    {'name': 'Julia', 'age': 19, 'grades': [4, 4, 5, 3]},
    {'name': 'Daniel', 'age': 25, 'grades': [2, 3, 2, 2]},
    {'name': 'Emma', 'age': 20, 'grades': [5, 5, 4, 4]},
    {'name': 'Peter', 'age': 21, 'grades': [4, 4, 3, 3]},
    {'name': 'Sophia', 'age': 22, 'grades': [3, 3, 5, 5]},
    {'name': 'James', 'age': 23, 'grades': [5, 5, 4, 4]},
    {'name': 'Lily', 'age': 19, 'grades': [4, 4, 3, 3]},
    {'name': 'Andrew', 'age': 20, 'grades': [3, 3, 2, 2]},
    {'name': 'Grace', 'age': 21, 'grades': [4, 4, 5, 5]}
]


students_20_years_old = list(filter(lambda student: student['age'] == 20, students))
everage_mark=list(map(lambda ev_mark: sum(ev_mark['grades'])/len(ev_mark['grades']), students))
all_ev_mark=sum(everage_mark)/len(everage_mark)
max_grade=list(filter(lambda student: sum(student['grades']) ==max(list(map(lambda ev_mark: sum(ev_mark['grades']),students)))  , students))


"""print("Студенты, которым 20 лет",students_20_years_old)
print("Средний бал каждого", everage_mark)
print("Средний бал общий",all_ev_mark)
print("Лучший средний бал",max_grade)"""

users = [
    {"name": "Nikolay", "expenses": [150, 4000, 23, 45]},
    {"name": "Anna", "expenses": [200, 300, 50, 1500]},
    {"name": "John", "expenses": [500, 100, 300, 200]},
    {"name": "Maria", "expenses": [1000, 2000, 500, 800]},
    {"name": "Michael", "expenses": [300, 700, 100, 50]},
    {"name": "Olga", "expenses": [250, 300, 400, 1000]},
    {"name": "David", "expenses": [700, 800, 1000, 200]},
    {"name": "Elena", "expenses": [1500, 3000, 500, 400]},
    {"name": "Alex", "expenses": [100, 50, 200, 1000]},
    {"name": "Sofia", "expenses": [300, 400, 150, 2000]},
    {"name": "Robert", "expenses": [200, 300, 400, 100]},
    {"name": "Julia", "expenses": [500, 700, 800, 2000]},
    {"name": "Daniel", "expenses": [800, 900, 1000, 700]},
    {"name": "Emma", "expenses": [2000, 2500, 3000, 500]},
    {"name": "Peter", "expenses": [500, 600, 700, 1500]},
    {"name": "Sophia", "expenses": [1000, 1200, 1500, 2500]},
    {"name": "James", "expenses": [700, 800, 900, 2000]},
    {"name": "Lily", "expenses": [600, 700, 800, 1200]},
    {"name": "Andrew", "expenses": [300, 400, 500, 1000]},
    {"name": "Grace", "expenses": [150, 200, 250, 700]}
]



sort_by= list(filter(lambda order: sum(order["expenses"])>4000, users))
total_expenses_per_user = list(map(lambda user: sum(user['expenses']), sort_by))
total_expenses_per_users = list(map(lambda user: sum(user['expenses']), users))


#print(sort_by)
#print(total_expenses_per_user)
#print(total_expenses_per_users)



orders = [
    {"order_id": 1, "customer_id": 101, "amount": 150},
    {"order_id": 2, "customer_id": 102, "amount": 200},
    {"order_id": 3, "customer_id": 103, "amount": 25},
    {"order_id": 4, "customer_id": 104, "amount": 300},
    {"order_id": 5, "customer_id": 105, "amount": 350},
    {"order_id": 6, "customer_id": 106, "amount": 400},
    {"order_id": 7, "customer_id": 101, "amount": 450},
    {"order_id": 8, "customer_id": 102, "amount": 500},
    {"order_id": 9, "customer_id": 103, "amount": 550},
    {"order_id": 10, "customer_id": 104, "amount": 600},
    {"order_id": 11, "customer_id": 105, "amount": 650},
    {"order_id": 12, "customer_id": 106, "amount": 700},
    {"order_id": 13, "customer_id": 101, "amount": 750},
    {"order_id": 14, "customer_id": 102, "amount": 800},
    {"order_id": 15, "customer_id": 103, "amount": 850},
    {"order_id": 16, "customer_id": 104, "amount": 900},
    {"order_id": 17, "customer_id": 105, "amount": 950},
    {"order_id": 18, "customer_id": 106, "amount": 1000},
    {"order_id": 19, "customer_id": 101, "amount": 1050},
    {"order_id": 20, "customer_id": 102, "amount": 1100}
]


sort_by_id= list(filter(lambda order: order["customer_id"] == 101, orders))
sum_of_ex=sum(list(map(lambda order: (order["amount"]), sort_by_id)))
avg_ex=sum(list(map(lambda order: (order["amount"]), sort_by_id)))/len(list(map(lambda order: (order["amount"]), sort_by_id)))

print(sort_by_id)
print(sum_of_ex)
print(avg_ex)