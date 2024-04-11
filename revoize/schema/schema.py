from datetime import datetime, timedelta
from enum import Enum
from typing import Dict, Optional

from pydantic import BaseModel, Field


class UserInfo(BaseModel):
    id: str
    time_used: timedelta = Field(validation_alias="timeUsed")
    user_plan: str = Field(validation_alias="userPlan")


class CognitoAuthenticationResult(BaseModel):
    access_token: str = Field(validation_alias="AccessToken")
    expires_in: int = Field(validation_alias="ExpiresIn")
    id_token: str = Field(validation_alias="IdToken")
    refresh_token: str = Field(validation_alias="RefreshToken")
    token_type: str = Field(validation_alias="TokenType")


class CognitoLoginResponse(BaseModel):
    authentication_result: CognitoAuthenticationResult = Field(
        validation_alias="AuthenticationResult"
    )
    # TODO: Improve handling of challenge parameters
    challenge_parameters: dict = Field(validation_alias="ChallengeParameters")


class Credentials(BaseModel):
    token: str

    @classmethod
    def from_cognito_login_response(
        cls, cognito_login_response: CognitoLoginResponse
    ) -> "Credentials":
        return Credentials(
            token=cognito_login_response.authentication_result.access_token
        )

    def as_auth_header(self) -> Dict[str, str]:
        return {"Authorization": f"Bearer {self.token}"}


class UploadedFileMetadata(BaseModel):
    etag: str
    upload_id: str


class UploadDetails(BaseModel):
    file_id: str = Field(validation_alias="fileId")
    upload_id: str = Field(validation_alias="uploadId")
    presigned_urls: Dict[str, str] = Field(validation_alias="presignedUrls")


class File(BaseModel):
    id: str
    name: str


class EnhancementStatus(Enum):
    FAILED = "FAILED"
    FINISHED = "FINISHED"
    PENDING = "PENDING"
    STARTED = "STARTED"


class FileUploadStatus(Enum):
    ABORTED = "ABORTED"
    COMPLETED = "COMPLETED"
    STARTED = "STARTED"


class EnhancementProcessingParameters(BaseModel):
    loudness: int = Field(ge=-32, le=-8)
    enhancement: int = Field(ge=0, le=100)


class EnhancementInputFile(BaseModel):
    id: str
    file_upload_status: FileUploadStatus = Field(validation_alias="fileUploadStatus")
    name: str


class EnhancementId(BaseModel):
    id: str


class EnhancementProcessStatus(EnhancementId):
    id: str
    input_file: EnhancementInputFile = Field(validation_alias="inputFile")
    parameters: EnhancementProcessingParameters
    status: EnhancementStatus


class Enhancement(EnhancementId):
    id: str
    audio_length: Optional[timedelta] = Field(validation_alias="audioLength")
    created_at: datetime = Field(validation_alias="createdAt")
    file_id: str = Field(validation_alias="fileId")
    file_name: str = Field(validation_alias="fileName")
    size_kb: Optional[int] = Field(validation_alias="sizeKb")
    status: EnhancementStatus


class DownloadLink(BaseModel):
    link: str


class EnhancementParameters(BaseModel):
    loudness: int = Field(default=-18, ge=-32, le=-8)
