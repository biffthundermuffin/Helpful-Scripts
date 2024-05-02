import os
import whisper

def transcribe_video(video_path, model_type='base', device='cuda'):
    model = whisper.load_model(model_type, device=device)
    result = model.transcribe(video_path)
    return result

def save_transcripts(result, output_file_path):
    transcript = result['text']
    with open(f'{output_file_path}.txt', 'w', encoding='utf-8') as text_file:
        text_file.write(transcript)
    
    with open(f'{output_file_path}.vtt', 'w', encoding='utf-8') as vtt_file:
        vtt_file.write("WEBVTT\n\n")
        for segment in result['segments']:
            start = format_timestamp(segment['start'])
            end = format_timestamp(segment['end'])
            text = segment['text'].replace('\n', ' ')
            vtt_file.write(f"{start} --> {end}\n{text}\n\n")

def format_timestamp(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = seconds % 60
    return f"{hours:02}:{minutes:02}:{seconds:06.3f}".replace('.', ',')

def read_transcribed_list(transcribed_list_file_path):
    if not os.path.exists(transcribed_list_file_path):
        return []
    
    with open(transcribed_list_file_path, 'r', encoding='utf-8') as file:
        transcribed_videos = file.read().splitlines()
    return transcribed_videos

def append_to_transcribed_list(transcribed_list_file_path, video_name):
    with open(transcribed_list_file_path, 'a', encoding='utf-8') as file:
        file.write(f"{video_name}\n")

def ensure_directory_exists(path):
    os.makedirs(path, exist_ok=True)  # Ensures the directory exists, creates it if it does not


def process_videos_in_directory(directory_path, output_path, model_type='base', device='cuda'):
    if not os.path.exists(output_path):
        os.makedirs(output_path, exist_ok=True)
    
    transcribed_list_file_path = os.path.join(success_path, 'transcribed.txt ')
    transcribed_videos = read_transcribed_list(transcribed_list_file_path)
    ensure_directory_exists(error_path)  # Ensure the error log directory exists
    error_log_path = os.path.join(error_path, 'errors.txt')
    
    for filename in os.listdir(directory_path):
        if filename.lower().endswith(('.mp4', '.mkv', '.avi', '.mov')) and filename not in transcribed_videos:
            video_path = os.path.join(directory_path, filename)
            base_filename_without_extension = os.path.splitext(filename)[0]
            output_file_path = os.path.join(output_path, base_filename_without_extension)
            try:
                print(f"Processing {filename} on {device}...")
                result = transcribe_video(video_path, model_type, device)
                save_transcripts(result, output_file_path)
                append_to_transcribed_list(transcribed_list_file_path, filename)  # Append successfully transcribed video name
                print(f"Finished processing {filename}.")
            except Exception as e:
                error_message = f"Failed to process {filename}: {e}\n"
                print(error_message)
                with open(error_log_path, 'a', encoding='utf-8') as error_file:
                    error_file.write(error_message)
    print(f"Updated list of successfully transcribed videos is maintained in {transcribed_list_file_path}")

# Example usage
directory_path = r'VIDEOPATH'
output_path = r'transcriptpath'
success_path = r'transcriptpath'
error_path = r'transcriptpath'
process_videos_in_directory(directory_path, output_path, model_type='medium', device='cuda')
