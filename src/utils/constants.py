class Constants:
    uploaded_files_path = "data/input/"
    query_quarters = """
        SELECT departments.department, 
               jobs.job,
               SUM(CASE WHEN MONTH(hired_employees.hire_date) BETWEEN 1 AND 3 THEN 1 ELSE 0 END) AS Q1,
               SUM(CASE WHEN MONTH(hired_employees.hire_date) BETWEEN 4 AND 6 THEN 1 ELSE 0 END) AS Q2,
               SUM(CASE WHEN MONTH(hired_employees.hire_date) BETWEEN 7 AND 9 THEN 1 ELSE 0 END) AS Q3,
               SUM(CASE WHEN MONTH(hired_employees.hire_date) BETWEEN 10 AND 12 THEN 1 ELSE 0 END) AS Q4
        FROM hired_employees
        INNER JOIN departments ON hired_employees.department_id = departments.id
        INNER JOIN jobs ON hired_employees.job_id = jobs.id
        WHERE YEAR(hired_employees.hire_date) = 2021
        GROUP BY departments.department, jobs.job
        ORDER BY departments.department, jobs.job;
    """
    query_more_hired = """
        SELECT departments.id, departments.department, COUNT(hired_employees.id) AS hired
        FROM departments
        INNER JOIN hired_employees ON departments.id = hired_employees.department_id
        WHERE YEAR(hired_employees.hire_date) = 2021
        GROUP BY departments.id, departments.department
        HAVING hired > (
            SELECT AVG(employees_count)
            FROM (
                SELECT COUNT(*) AS employees_count
                FROM hired_employees
                WHERE YEAR(hire_date) = 2021
                GROUP BY department_id
            ) AS department_avg
        )
        ORDER BY hired DESC;
    """
    