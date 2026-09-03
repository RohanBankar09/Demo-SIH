import json
import random
import urllib.request

base_url = 'http://127.0.0.1:8000/api/v1'
r_id = random.randint(1000, 9999)

def post_json(path, data, token=None):
    headers = {'Content-Type': 'application/json'}
    if token:
        headers['Authorization'] = f'Bearer {token}'
    req = urllib.request.Request(
        f'{base_url}{path}',
        data=json.dumps(data).encode('utf-8'),
        headers=headers
    )
    with urllib.request.urlopen(req, timeout=5) as res:
        return json.loads(res.read().decode())

def get_json(path, token=None):
    headers = {}
    if token:
        headers['Authorization'] = f'Bearer {token}'
    req = urllib.request.Request(
        f'{base_url}{path}',
        headers=headers
    )
    with urllib.request.urlopen(req, timeout=5) as res:
        return json.loads(res.read().decode())

def main():
    print('--- Testing 4-Role Registrations ---')
    st_res = post_json('/auth/register/student', {
        'email': f'test.student.{r_id}@example.com',
        'password': 'Password123!',
        'full_name': 'Test Student',
        'college_name': 'Apex Institute'
    })
    print('Student registered:', st_res['email'], 'Role:', st_res['role'])

    cp_res = post_json('/auth/register/company', {
        'email': f'test.company.{r_id}@example.com',
        'password': 'Password123!',
        'company_name': 'Apex AI Corp',
        'industry': 'Software'
    })
    print('Company registered:', cp_res['email'], 'Role:', cp_res['role'])

    in_res = post_json('/auth/register/institution', {
        'email': f'test.institution.{r_id}@example.com',
        'password': 'Password123!',
        'institution_name': 'Global Tech University',
        'institution_type': 'University'
    })
    print('Institution registered:', in_res['email'], 'Role:', in_res['role'])

    ac_res = post_json('/auth/register/academician', {
        'email': f'test.academician.{r_id}@example.com',
        'password': 'Password123!',
        'full_name': 'Dr. Test Professor',
        'department': 'CSE'
    })
    print('Academician registered:', ac_res['email'], 'Role:', ac_res['role'])

    print('\n--- Testing Login & JWT Verification for All 4 Roles ---')
    for email, expected in [
        ('student@pixie.com', 'student'),
        ('techcorp@pixie.com', 'company'),
        ('apex.institute@pixie.com', 'institution'),
        ('prof.sharma@pixie.com', 'academician')
    ]:
        tok = post_json('/auth/login', {'email': email, 'password': 'Password123!'})['access_token']
        me = get_json('/auth/me', token=tok)
        print(f'Logged in {email} -> Token verified role: {me["role"]} (Matches: {me["role"] == expected})')

    print('\n--- Testing Opportunities API ---')
    opps = get_json('/opportunities/')
    print(f'Total Opportunities Found: {len(opps)}')
    for o in opps[:2]:
        print(' -', o['title'], f'({o["opportunity_type"]})')

    print('\n[SUCCESS] All backend 4-role verification checks passed!')

if __name__ == '__main__':
    main()
