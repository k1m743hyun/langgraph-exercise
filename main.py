from langgraph.graph import StateGraph
from typing import TypedDict, Dict, Any
from datetime import datetime

class DataState(TypedDict):
    raw_data: str
    process_data: dict
    metadata: dict

def data_processor_node(state: DataState) -> Dict[str, Any]:
    '''
    상태 처리 노드
    원시 데이터를 받아 구조화된 데이터로 변환
    '''
    raw_data = state["raw_data"]

    # 데이터 파싱
    lines = raw_data.strip().split('\n')

    # 구조화
    processed = {
        "total_lines": len(lines),
        "content": lines,
        "first_line": lines[0] if lines else "",
        "last_line": lines[-1] if lines else "",
    }

    # 메타데이터 생성
    metadata = {
        "processed_at": datetime.now().isoformat(),
        "processor_version": "1.0.0",
        "data_size": len(raw_data),
    }

    return {
        "process_data": processed,
        "metadata": metadata,
    }