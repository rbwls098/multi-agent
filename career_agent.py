import json
from pathlib import Path

# =====================================
# 1단계: 사용자 프로필 추출
# =====================================

def extract_profile(profile_file="sample_career_profile.json"):
    """
    사용자 프로필 JSON을 읽고 핵심 정보를 추출한다.
    
    출력: [{user_id, name, years, skills, interests}, ...]
    """
    with open(profile_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    extracted = []
    for profile in data['profiles']:
        user_info = {
            'user_id': profile['id'],
            'name': profile['name'],
            'experience_years': profile['experience']['years'],
            'skills': profile['skills']['programming_languages'] + 
                     profile['skills']['frameworks'],
            'interests': profile['interests'],
            'education': profile['education']['major'],
            'certifications': profile['certifications']
        }
        extracted.append(user_info)
    
    return extracted


# =====================================
# 2단계: 사용자-공고 매칭 및 분류
# =====================================

def classify_user(profiles, opportunities_file="sample_data/opportunities.json"):
    """
    각 사용자를 분류하고 관련 공고를 매칭한다.
    
    입력: 추출된 프로필 리스트
    출력: [{user_id, name, job_type, matched_opportunities}, ...]
    """
    with open(opportunities_file, 'r', encoding='utf-8') as f:
        opps = json.load(f)['opportunities']
    
    classified = []
    
    for profile in profiles:
        # 관심사와 스킬로 직무 유형 결정
        job_type = determine_job_type(profile['interests'])
        
        # 사용자에게 맞는 공고 매칭
        matched = []
        for opp in opps:
            score = calculate_match_score(profile, opp)
            if score >= 0.5:  # 50% 이상 매칭
                matched.append({
                    'opp_id': opp['id'],
                    'title': opp['title'],
                    'company': opp['company'],
                    'match_score': round(score, 2),
                    'category': opp['category']
                })
        
        # 점수순 정렬
        matched.sort(key=lambda x: x['match_score'], reverse=True)
        
        classified.append({
            'user_id': profile['user_id'],
            'name': profile['name'],
            'job_type': job_type,
            'experience_years': profile['experience_years'],
            'matched_opportunities': matched[:3]  # 상위 3개만
        })
    
    return classified


def determine_job_type(interests):
    """사용자 관심사로 직무 유형 판단"""
    interests_lower = [i.lower() for i in interests]
    
    if any('웹' in i or '프론트' in i or 'react' in i.lower() for i in interests_lower):
        return '웹개발'
    elif any('ai' in i.lower() or '머신' in i or '데이터' in i for i in interests_lower):
        return '데이터/AI'
    elif any('리더' in i or '비즈' in i or '매니저' in i for i in interests_lower):
        return '비즈니스개발'
    else:
        return '기타'


def calculate_match_score(profile, opportunity):
    """사용자와 공고의 매칭 점수 계산 (0~1)"""
    score = 0
    
    # 1. 기술 매칭
    required_skills = opportunity['required_skills']
    user_skills = profile['skills']
    
    matching_skills = 0
    for req_skill in required_skills:
        if any(req_skill.lower() in user_skill.lower() 
               or user_skill.lower() in req_skill.lower() 
               for user_skill in user_skills):
            matching_skills += 1
    
    skill_score = matching_skills / len(required_skills) if required_skills else 0
    score += skill_score * 0.6
    
    # 2. 관심사 매칭
    category = opportunity['category'].lower()
    interests_match = any(interest.lower() in category 
                         or category in interest.lower()
                         for interest in profile['interests'])
    score += (0.4 if interests_match else 0)
    
    # 3. 경력 요구사항
    if profile['experience_years'] >= opportunity['experience_years']:
        score *= 1.1  # 10% 보너스
    
    return min(score, 1.0)


# =====================================
# 3단계: 최종 추천문 작성
# =====================================

def write_recommendations(classified_users):
    """
    각 사용자별 추천 안내문과 자소서 팁을 작성한다.
    
    입력: 분류된 사용자 리스트
    출력: Markdown 형식의 추천 가이드
    """
    output = "# 취업 안내 - 맞춤형 추천\n\n"
    
    for user in classified_users:
        output += f"## {user['name']} - {user['job_type']} 직무\n\n"
        output += f"**경력:** {user['experience_years']}년\n\n"
        
        if not user['matched_opportunities']:
            output += "현재 적합한 공고가 없습니다. 기술 강화를 권장합니다.\n\n"
            continue
        
        output += "### 추천 공고\n\n"
        for idx, opp in enumerate(user['matched_opportunities'], 1):
            output += f"{idx}. **{opp['title']}** ({opp['company']})\n"
            output += f"   - 분야: {opp['category']}\n"
            output += f"   - 매칭도: {int(opp['match_score']*100)}%\n"
            output += f"   - 💡 **자소서 팁**: "
            
            # 분야별 팁
            if '개발' in opp['category']:
                output += "기술 프로젝트와 깃허브 활동을 강조하세요.\n"
            elif 'AI' in opp['category'] or '데이터' in opp['category']:
                output += "데이터 분석 프로젝트와 머신러닝 경험을 강조하세요.\n"
            else:
                output += "리더십과 전략 기획 경험을 강조하세요.\n"
            
            output += "\n"
        
        output += "---\n\n"
    
    return output


# =====================================
# 메인 실행
# =====================================

def main():
    print("=" * 60)
    print("취업 안내 멀티에이전트 v0 시작")
    print("=" * 60)
    print()
    
    # Step 1: 프로필 추출
    print("[Step 1] 사용자 프로필 추출...")
    profiles = extract_profile()
    print(f"✓ {len(profiles)}명의 사용자 정보 추출됨\n")
    
    for profile in profiles:
        print(f"  - {profile['name']}: {profile['experience_years']}년 경력, "
              f"{', '.join(profile['interests'])} 관심")
    print()
    
    # Step 2: 분류 및 매칭
    print("[Step 2] 사용자 분류 및 공고 매칭...")
    classified = classify_user(profiles)
    print(f"✓ 사용자 분류 및 매칭 완료\n")
    
    for user in classified:
        print(f"  - {user['name']}: {user['job_type']} | "
              f"{len(user['matched_opportunities'])}개 공고 매칭")
        for opp in user['matched_opportunities']:
            print(f"      → {opp['title']} ({int(opp['match_score']*100)}%)")
    print()
    
    # Step 3: 최종 추천문 작성
    print("[Step 3] 최종 추천안내문 작성...")
    recommendations = write_recommendations(classified)
    print("✓ 추천안내문 생성 완료\n")
    
    # 결과 출력
    print("=" * 60)
    print("최종 결과")
    print("=" * 60)
    print(recommendations)
    
    return recommendations


if __name__ == "__main__":
    result = main()
    
    # 결과를 파일로 저장 (선택사항)
    # with open('career_recommendations.md', 'w', encoding='utf-8') as f:
    #     f.write(result)
