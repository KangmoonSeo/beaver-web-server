"""
저장 공간 관리에 사용되는 비즈니스 로직을 담은 코드 페이지입니다. 
"""

import os

from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

from .session import get_user_id


TABLE_EXT = [".csv", ".tsv", ".xlsx"]


def get_storage_path() -> str:
    """
    storage path를 가져옵니다.
    """
    user_id = get_user_id()
    storage_path = os.path.join("./server/storage", str(user_id))
    return storage_path


async def clear_storage() -> None:
    """
    저장소를 비웁니다.
    """
    storage_path = get_storage_path()
    raw_path = os.path.join(storage_path, "raw")
    embed_path = os.path.join(storage_path, "embed")
    structured_path = os.path.join(storage_path, "structured")

    # 기존 디렉토리 및 하위 내용 삭제
    if os.path.exists(storage_path):
        for root, dirs, files in os.walk(storage_path, topdown=False):
            for file_name in files:
                os.remove(os.path.join(root, file_name))
            for dir_name in dirs:
                os.rmdir(os.path.join(root, dir_name))
        os.rmdir(storage_path)

    #  디렉토리 재생성
    os.makedirs(raw_path)
    os.makedirs(embed_path)
    os.makedirs(structured_path)


async def save_file(contents: bytes, filename: str, description: str) -> None:
    """
    파일을 확장자에 맞추어 저장합니다.
    """

    file_path = None
    file_ext = None
    storage_path = get_storage_path()

    # 확장자 추출
    _, file_ext = os.path.splitext(filename)
    new_filename = f"{description}{file_ext}"

    if file_ext.lower() in TABLE_EXT:
        file_path = os.path.join(storage_path, "structured", new_filename)
    else:
        file_path = os.path.join(storage_path, "raw", new_filename)

    with open(file_path, "wb") as fp:
        fp.write(contents)


async def load_table_filename() -> str | None:
    """
    path에 있는 첫 번째 테이블 파일 경로를 전달하는 함수
    """
    storage_path = get_storage_path()
    structured_path = os.path.join(storage_path, "structured")

    files = os.listdir(structured_path)

    # 지원하는 확장자를 가진 파일 찾기
    table_file = next(
        (file for file in files if any(file.endswith(ext) for ext in TABLE_EXT)), None
    )

    if not table_file:
        return None

    table_file_path = os.path.join(structured_path, table_file)

    return table_file_path


async def load_embed_index() -> Chroma:
    """
    임베딩 벡터 데이터를 가져와 인덱스를 호출합니다.
    """
    storage_path = get_storage_path()
    embed_path = os.path.join(storage_path, "embed")

    try:
        """
        chroma 로 부터 벡터스토어 인덱스를 호출합니다.
        """
        vectorstore = Chroma(persist_directory="./chroma_db", embedding=OpenAIEmbeddings())

        return vectorstore
    except FileNotFoundError:  # 사용자로부터 임베딩 파일을 받지 못했을 때 예외를 표출함
        return None
