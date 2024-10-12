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

def process_videos_in_directory(directory_path, model_type='base', device='cuda'):
    # Automatically generate paths for output, success, and error
    output_path = os.path.join(directory_path, 'output')
    success_path = os.path.join(output_path, 'success')
    error_path = os.path.join(output_path, 'error')
    
    ensure_directory_exists(output_path)
    ensure_directory_exists(success_path)
    ensure_directory_exists(error_path)

    transcribed_list_file_path = os.path.join(success_path, 'transcribed.txt')
    transcribed_videos = read_transcribed_list(transcribed_list_file_path)
    
    error_log_path = os.path.join(error_path, 'errors.txt')

    # List of common video formats
    video_formats = ('.mp4', '.mkv', '.avi', '.mov', '.webm', '.flv', '.wmv', '.m4v', '.mpeg', '.mpg', '.3gp', '.m2ts')

    for root, _, files in os.walk(directory_path):  # Recursively walk through the directory
        for filename in files:
            if filename.lower().endswith(video_formats) and filename not in transcribed_videos:
                video_path = os.path.join(root, filename)
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
directory_path = r'path to videos '
process_videos_in_directory(directory_path, model_type='medium', device='cuda')
