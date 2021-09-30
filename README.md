# awsproject

<myproject 이식 시, python command Not Found 해결 방법>
- 가끔, python이 환경변수 상에 추가되었는데, 가상환경에 타인 업로드한 가상환경에 진입 시,python 명령어가 인식되지 않는 경우가 있습니다.
- 1. 본인만의 가상환경 파일을 만들기
     => 본인 컴퓨터에서 직접 가상환경을 구축하는 방법입니다. 
     => python -m venv mysite
          : mysite 은 가상환경의 이름이니, 원하시는 이름으로 하면 됩니다.   

<ModuleNotFoundError: No module named 'widget_tweaks' 에러 해결 방법>
- pip install django-widget-tweaks 

<Cannot use ImageField because Pillow is not installed. 에러 해결방법>
- pip install Pillow

<ORM 데이터 모델 적용위한 파일 생성 - 이미 있으면 안만들어도 됨>
- 각각의 App 폴더 (우리의 경우, blog 디렉토리) 내에 0001_initial.py 파일 존재하면, 아래 명령어 실행하지 않아도 됨
- python manage.py makemigrations

<SqlLite3에 실제 Table 생성>
- python manage.py migrate

<최종적으로... 서버 실행>
- python manage.py runserver 
