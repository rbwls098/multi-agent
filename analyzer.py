import json

class CompetencyAnalysisAgent:
    def __init__(self, profile_path="sample_career_profile.json"):
        self.profile_path = profile_path

    def run(self):
        print(f"[역량 분석 에이전트] 사용자 프로필을 분석합니다 (소스: {self.profile_path})")
        with open(self.profile_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        analyzed_profiles = []
        for profile in data.get('profiles', []):
            interests = profile.get('interests', [])
            job_type = self._determine_job_type(interests)
            
            analyzed = {
                'user_id': profile['id'],
                'name': profile['name'],
                'experience_years': profile['experience']['years'],
                'skills': profile['skills']['programming_languages'] + profile['skills']['frameworks'],
                'interests': interests,
                'education': profile['education']['major'],
                'certifications': profile['certifications'],
                'job_type': job_type
            }
            analyzed_profiles.append(analyzed)
        
        print(f"✓ 총 {len(analyzed_profiles)}명의 사용자 역량 분석을 완료했습니다.\n")
        return analyzed_profiles

    def _determine_job_type(self, interests):
        has_web = any('웹' in i or '프론트' in i or 'react' in i.lower() for i in interests)
        has_ai = any('ai' in i.lower() or '머신' in i or '데이터' in i for i in interests)
        has_biz = any('리더' in i or '비즈' in i or '매니저' in i for i in interests)
        
        if has_web:
            return '웹개발'
        elif has_ai:
            return '데이터/AI'
        elif has_biz:
            return '비즈니스개발'
        else:
            return '기타'
