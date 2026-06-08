import json

class CompetencyAnalysisAgent:
    def __init__(self, profile_path="sample_career_profile.json"):
        self.profile_path = profile_path

    def run(self):
        print(f"[역량 분석 에이전트] 사용자 프로필을 분석합니다.")
        with open(self.profile_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        analyzed_profiles = []
        for profile in data.get('profiles', []):
            interests = profile.get('interests', [])
            # 4개 카테고리 제한을 풀고 사용자의 첫 번째 관심사를 주 직무로 설정
            job_type = interests[0] if interests else "미지정"
            
            # 기술 스택 추출 강화
            all_skills = []
            if 'skills' in profile:
                if isinstance(profile['skills'], dict):
                    for val in profile['skills'].values():
                        all_skills.extend(val if isinstance(val, list) else [val])
                else:
                    all_skills.extend(profile['skills'])
            
            if 'experience' in profile and 'positions' in profile['experience']:
                for pos in profile['experience']['positions']:
                    all_skills.extend(pos.get('skills', []))

            analyzed = {
                'user_id': profile['id'],
                'name': profile['name'],
                'experience_years': profile.get('experience', {}).get('years', 0),
                'skills': list(set(all_skills)), # 중복 제거
                'interests': interests,
                'job_type': job_type
            }
            analyzed_profiles.append(analyzed)
        
        print(f"✓ {len(analyzed_profiles)}명의 역량 분석을 완료했습니다. (주 직무: {job_type})\n")
        return analyzed_profiles
