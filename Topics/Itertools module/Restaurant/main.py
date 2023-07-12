import itertools

main_courses = ['beef stew', 'fried fish']
price_main_courses = [28, 23]
desserts = ['ice-cream', 'cake']
price_desserts = [2, 4]
drinks = ['cola', 'wine']
price_drinks = [3, 10]

for i in itertools.product(main_courses, desserts, drinks):
    m, d, r = i
    total = price_main_courses[main_courses.index(m)]+price_desserts[desserts.index(d)]+price_drinks[drinks.index(r)]
    if total <= 30:
        print(m,d,r,total)