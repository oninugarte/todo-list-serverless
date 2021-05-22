import boto3
import click

@click.command()
@click.option('--phrase', prompt='Put in any language to translate', help='this is a tool that translates text')

def translate(phrase):
    client = boto3.client('translate', region_name = "us-east-1")
    click.echo(click.style(f"Translate phrase: {phrase}", fg='red'))
    result = client.translate_text(Text=phrase, SourceLanguageCode='auto', TargetLanguageCode="en")
    text = result['TranslatedText']
    click.echo(click.style(f'{text}', bg='blue', fg='white'))
    
if __name__=='__main__':
    translate()