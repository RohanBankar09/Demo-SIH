import json
import random
import urllib.error
import urllib.request

base_url = 'http://127.0.0.1:8000/api/v1'

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
    print('=== PIXIE PHASE 2: COMPLETE STUDENT ASSESSMENT FLOW E2E TEST ===\n')

    # 1. Login as student
    print('[Step 1] Logging in as student...')
    login_res = post_json('/auth/login', {
        'email': 'student@pixie.com',
        'password': 'Password123!'
    })
    token = login_res['access_token']
    print(' -> JWT Token acquired successfully.')

    # 2. Get User & StudentProfile
    print('\n[Step 2] Retrieving student identity and profile...')
    user = get_json('/auth/me', token=token)
    profile = get_json('/students/me', token=token)
    print(f" -> User ID: {user['id']}, Email: {user['email']}, Role: {user['role']}")
    print(f" -> StudentProfile ID: {profile['id']}, Full Name: {profile['full_name']}, College: {profile['college_name']}")

    # 3. Fetch Assessment Catalog
    print('\n[Step 3] Fetching assessment catalog (GET /api/v1/assessments/)...')
    assessments = get_json('/assessments/', token=token)
    print(f' -> Found {len(assessments)} active assessments:')
    for a in assessments:
        print(f"    - ID #{a['id']}: {a['title']} ({a['difficulty'].upper()}, {a['time_limit_minutes']} mins)")
    assert len(assessments) > 0, 'No assessments available!'
    target_assessment = assessments[0]

    # 4. Fetch Assessment Questions & Options
    print(f"\n[Step 4] Fetching questions for Assessment #{target_assessment['id']} (GET /api/v1/assessments/{target_assessment['id']}/questions)...")
    questions = get_json(f"/assessments/{target_assessment['id']}/questions", token=token)
    print(f' -> Found {len(questions)} questions for this assessment:')
    for idx, q in enumerate(questions):
        print(f"    Q{idx+1} [ID:{q['id']}]: {q['question_text']} ({q['marks']} marks)")
        for opt in q['options']:
            print(f"       Option [ID:{opt['id']}]: {opt['option_text']}")

    # 5. Start Attempt
    print(f"\n[Step 5] Starting assessment attempt (POST /api/v1/attempts/start)...")
    attempt = post_json('/attempts/start', {
        'assessment_id': target_assessment['id'],
        'student_id': profile['id']
    }, token=token)
    attempt_id = attempt['id']
    print(f" -> Attempt initialized: ID #{attempt_id}, Status: {attempt['status']}, Max Score: {attempt['max_score']}")

    # 6. Submit Assessment Answers
    print(f"\n[Step 6] Submitting answers for Attempt #{attempt_id} (POST /api/v1/attempts/{attempt_id}/submit)...")
    answers_payload = []
    for q in questions:
        # Select first option for each question
        selected_opt = q['options'][0]['id']
        answers_payload.append({
            'question_id': q['id'],
            'selected_option_id': selected_opt,
            'answer_text': None
        })
    
    submit_res = post_json(f'/attempts/{attempt_id}/submit', {
        'answers': answers_payload
    }, token=token)
    print(f" -> Submission successful! Status: {submit_res['status']}, Score: {submit_res['score']}/{submit_res['max_score']} ({submit_res['percentage']}%)")

    # 7. Get Official Attempt Result
    print(f"\n[Step 7] Retrieving official result report (GET /api/v1/attempts/{attempt_id}/result)...")
    result_res = get_json(f'/attempts/{attempt_id}/result', token=token)
    print(f" -> Result Report: Attempt #{result_res['attempt_id']}")
    print(f"    Assessment: {result_res['assessment_title']}")
    print(f"    Score: {result_res['score']} / {result_res['max_score']}")
    print(f"    Percentage: {result_res['percentage']}%")
    print(f"    Status: {result_res['status']}")
    print(f"    Completed At: {result_res['completed_at']}")

    # 8. Get Student's Past Attempts History (My Results)
    print('\n[Step 8] Retrieving student assessment history (GET /api/v1/attempts/me)...')
    my_attempts = get_json('/attempts/me', token=token)
    print(f' -> Total attempts in student history: {len(my_attempts)}')
    found = any(a['attempt_id'] == attempt_id for a in my_attempts)
    print(f' -> Newly completed Attempt #{attempt_id} present in history: {found}')
    assert found, 'Newly completed attempt not found in student history!'

    print('\n=================================================================')
    print('[SUCCESS] ALL 8 STEPS OF THE STUDENT ASSESSMENT FLOW PASSED!')
    print('=================================================================')

if __name__ == '__main__':
    main()
