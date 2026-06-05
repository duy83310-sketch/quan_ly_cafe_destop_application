import os

def clean_comments(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    new_lines = []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith('#'):
            continue
        
        if '#' in line:
            idx = line.find('#')
            prefix = line[:idx]
            if prefix.count('"') % 2 == 0 and prefix.count("'") % 2 == 0:
                line = prefix.rstrip() + '\n'
                if not line.strip():
                    continue
        new_lines.append(line)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)

for root, dirs, files in os.walk('d:/Du_an_CNTT/Lap_trinh_python/App_cafe_op2/src'):
    for file in files:
        if file.endswith('.py'):
            clean_comments(os.path.join(root, file))
print('Done!')
