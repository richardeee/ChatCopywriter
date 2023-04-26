import requests
import time
import os
from pydantic import BaseModel, Extra, root_validator
from langchain.utils import get_from_dict_or_env

from typing import Dict, List

import requests

class Dalle2Helper(BaseModel):
    dalle2_api_version = '2022-08-03-preview'

    dalle_api_key: str
    dalle_api_url: str
    
    class Config:
        """Configuration for this pydantic object."""

        extra = Extra.forbid

    def run(self, user_prompt: str) -> str:
        """Run user prompt through Dalle and return image url."""
        url = "{api_base}dalle/text-to-image?api-version={api_version}".format(api_base=self.dalle_api_url, api_version='2022-08-03-preview')
        headers= { "api-key": self.dalle_api_key, "Content-Type": "application/json" }
        body = {
            "caption": user_prompt,
            "resolution": "{height}x{width}".format(height=512, width=512),
        }
        print(user_prompt)
        submission = requests.post(url, headers=headers, json=body)
        operation_location = submission.headers['Operation-Location']
        retry_after = submission.headers['Retry-after']
        status = ""
        while (status != "Succeeded"):
            time.sleep(int(retry_after))
            response = requests.get(operation_location, headers=headers)
            status = response.json()['status']
        image_url = response.json()['result']['contentUrl']
        return image_url

    

    @root_validator(pre=True)
    def validate_environment(cls, values: Dict) -> Dict:
        """Validate that api key and endpoint exists in environment."""
        dalle_api_key = get_from_dict_or_env(
            values, "dalle_api_key","DALLE_API_KEY"
        )
        values["dalle_api_key"] = dalle_api_key

        dalle_api_url = get_from_dict_or_env(
            values,
            "dalle_api_url",
            "DALLE_API_URL",
        )

        values["dalle_api_url"] = dalle_api_url

        return values

