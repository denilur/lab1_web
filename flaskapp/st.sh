language: python
before_install:
 - chmod +x ./flaskapp/st.sh
install:
 - pip3 install flask
 - pip3 install gunicorn
 - pip3 install requests
script:
 - cd flaskapp
 - ./st.sh 
