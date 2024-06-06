from setuptools import find_packages, setup
setup(
    name="Report-Generator",
    version="0.0.1",
    author="Barath",
    author_email="paramasivanbarath1011@gmail.com",
    install_requires=["youtube_transcript_api","streamlit","python-dotenv","google-generativeai","pathlib"],
    packages=find_packages()
)




