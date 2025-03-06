import asyncio
import io
import logging
from openai import AsyncOpenAI


async def convert_to_mp3(audio: bytes) -> bytes:
    try:
        process = await asyncio.create_subprocess_exec(
            'ffmpeg',
            '-i',
            'pipe:0',
            '-f',
            'mp3',
            '-acodec',
            'libmp3lame',
            '-b:a',
            '128k',
            'pipe:1',
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await process.communicate(input=audio)
        if process.returncode != 0:
            raise RuntimeError(f"FFmpeg failed: {stderr.decode()}")
        return stdout
    except FileNotFoundError:
        logging.error("FFmpeg is not installed or not found in PATH.")
        raise RuntimeError("FFmpeg is not installed or not found in PATH.")


async def transcribe_audio(audio_file, openai_client: AsyncOpenAI) -> str | None:
    try:
        ogg_audio = audio_file.read()
        mp3_audio = await convert_to_mp3(ogg_audio)
        audio_stream = io.BytesIO(mp3_audio)
        audio_stream.name = 'audio.mp3'
        transcript = await openai_client.audio.transcriptions.create(
            file=audio_stream, model="whisper-1", response_format="text"
        )
        return transcript if transcript else None

    except Exception as e:
        logging.exception(f"Error in transcription: {e}")
        return None
