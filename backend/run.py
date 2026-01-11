"""
Run Flask development server
"""

from app import create_app

app = create_app('development')

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🚀 InnSight API Server Starting...")
    print("="*60)
    print(f"API running at: http://localhost:{app.config['API_PORT']}")
    print("Press CTRL+C to stop")
    print("="*60 + "\n")
    
    app.run(
        host='0.0.0.0',
        port=app.config['API_PORT'],
        debug=app.config['DEBUG']
    )