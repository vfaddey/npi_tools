from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Optional
from uuid import UUID



@dataclass
class File:
    id: UUID
    filename: str
    uploaded_at: datetime
    is_public: bool
    user_id: UUID
    file_hash: Optional[str] = None

    def dump(self):
        return asdict(self)
