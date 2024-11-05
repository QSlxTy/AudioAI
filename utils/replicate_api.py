import logging
import os
import random
from datetime import datetime

import replicate
from docx import Document

from integrations.database.models.decoding import create_decoding_db, update_decoding_db
from src.config import Configuration

REPLICATE_API_TOKEN = Configuration.replicate_token

os.environ["REPLICATE_API_TOKEN"] = REPLICATE_API_TOKEN


async def replicate_func(audio, lang, speakers, words, format_decoding, user_id, session_maker):
    logging.info(f"Start decoding")
    file = open(audio, "rb")
    replicate_id = int(random.randint(1, 999999))
    await create_decoding_db(user_id, 'in_process', replicate_id, session_maker)
    try:
        if lang == '':
            if speakers == '':
                output = await replicate.async_run(
                    "thomasmol/whisper-diarization:80648d30772b580c9528f51592a827b850dd42269fe92881f9084d916e67617f",
                    input={
                        "file": file,
                        "prompt": words,
                        "group_segments": True,
                        "offset_seconds": 0,
                        "transcript_output_format": "segments_only"
                    }
                )
            else:
                output = await replicate.async_run(
                    "thomasmol/whisper-diarization:80648d30772b580c9528f51592a827b850dd42269fe92881f9084d916e67617f",
                    input={
                        "file": file,
                        "prompt": words,
                        "group_segments": True,
                        "num_speakers": speakers,
                        "offset_seconds": 0,
                        "transcript_output_format": "segments_only"
                    }
                )
        else:
            if speakers == '':
                output = await replicate.async_run(
                    "thomasmol/whisper-diarization:80648d30772b580c9528f51592a827b850dd42269fe92881f9084d916e67617f",
                    input={
                        "file": file,
                        "prompt": words,
                        "language": lang,
                        "group_segments": True,
                        "offset_seconds": 0,
                        "transcript_output_format": "segments_only"
                    }
                )
            else:
                output = await replicate.async_run(
                    "thomasmol/whisper-diarization:80648d30772b580c9528f51592a827b850dd42269fe92881f9084d916e67617f",
                    input={
                        "file": file,
                        "prompt": words,
                        "language": lang,
                        "group_segments": True,
                        "num_speakers": speakers,
                        "offset_seconds": 0,
                        "transcript_output_format": "segments_only"
                    }
                )
        await update_decoding_db(user_id, replicate_id, {'status': 'done'}, session_maker)
        logging.info(f"Decoding success")
        doc = Document()
        if 'Расшифровка с тайм-кодами и разбиением на спикеров' == format_decoding:
            def format_time(seconds):
                hours = int(seconds // 3600)
                minutes = int((seconds % 3600) // 60)
                seconds = seconds % 60
                return f"{hours:02}:{minutes:02}:{seconds:05.2f}".replace('.', ':')

            for segment in output['segments']:
                start_time = format_time(segment['start'])
                end_time = format_time(segment['end'])
                speaker = segment['speaker']
                text = segment['text']
                doc.add_paragraph(f"[{start_time} - {end_time} - {speaker}]")
                doc.add_paragraph(text)
                doc.add_paragraph("")
        else:
            for segment in output['segments']:
                text = segment['text']
                doc.add_paragraph(text)
        doc.save(f"media/{user_id}/{str(datetime.now()).split(' ')[0]}_СлушАЙ.docx")
        return audio, f"media/{user_id}/{str(datetime.now()).split(' ')[0]}_СлушАЙ.docx"
    except Exception as _ex:
        logging.error(f"Decoding error: {_ex}")
        await update_decoding_db(user_id, replicate_id, {'status': 'error'}, session_maker)
        return None


async def replicate_func_url(audio, lang, speakers, words, format_decoding, user_id, session_maker):
    logging.info(f"Start decoding")
    replicate_id = int(random.randint(1, 999999))
    await create_decoding_db(user_id, 'in_process', replicate_id, session_maker)
    try:
        if lang == '':
            if speakers == '':
                output = await replicate.async_run(
                    "thomasmol/whisper-diarization:80648d30772b580c9528f51592a827b850dd42269fe92881f9084d916e67617f",
                    input={
                        "file_url": audio,
                        "prompt": words,
                        "group_segments": True,
                        "offset_seconds": 0,
                        "transcript_output_format": "segments_only"
                    }
                )
            else:
                output = await replicate.async_run(
                    "thomasmol/whisper-diarization:80648d30772b580c9528f51592a827b850dd42269fe92881f9084d916e67617f",
                    input={
                        "file_url": audio,
                        "prompt": words,
                        "group_segments": True,
                        "num_speakers": speakers,
                        "offset_seconds": 0,
                        "transcript_output_format": "segments_only"
                    }
                )
        else:
            if speakers == '':
                output = await replicate.async_run(
                    "thomasmol/whisper-diarization:80648d30772b580c9528f51592a827b850dd42269fe92881f9084d916e67617f",
                    input={
                        "file_url": audio,
                        "prompt": words,
                        "language": lang,
                        "group_segments": True,
                        "offset_seconds": 0,
                        "transcript_output_format": "segments_only"
                    }
                )
            else:
                output = await replicate.async_run(
                    "thomasmol/whisper-diarization:80648d30772b580c9528f51592a827b850dd42269fe92881f9084d916e67617f",
                    input={
                        "file_url": audio,
                        "prompt": words,
                        "language": lang,
                        "group_segments": True,
                        "num_speakers": speakers,
                        "offset_seconds": 0,
                        "transcript_output_format": "segments_only"
                    }
                )
        await update_decoding_db(user_id, replicate_id, {'status': 'done'}, session_maker)
        logging.info(f"Decoding success")
        doc = Document()
        if 'Расшифровка с тайм-кодами и разбиением на спикеров' == format_decoding:
            def format_time(seconds):
                hours = int(seconds // 3600)
                minutes = int((seconds % 3600) // 60)
                seconds = seconds % 60
                return f"{hours:02}:{minutes:02}:{seconds:05.2f}".replace('.', ':')

            for segment in output['segments']:
                start_time = format_time(segment['start'])
                end_time = format_time(segment['end'])
                speaker = segment['speaker']
                text = segment['text']
                doc.add_paragraph(f"[{start_time} - {end_time} - {speaker}]")
                doc.add_paragraph(text)
                doc.add_paragraph("")
        else:
            for segment in output['segments']:
                text = segment['text']
                doc.add_paragraph(text)
        doc.save(f"media/{user_id}/{str(datetime.now()).split(' ')[0]}_СлушАЙ.docx")
        return f"media/{user_id}/{str(datetime.now()).split(' ')[0]}_СлушАЙ.docx"
    except Exception as _ex:
        logging.error(f"Decoding error: {_ex}")
        await update_decoding_db(user_id, replicate_id, {'status': 'error'}, session_maker)
        return None