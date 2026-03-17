import fs from 'fs';
import path from 'path';

/**
 * Vite插件：构建完成后自动复制到ui目录
 */
export default function copyToUiPlugin() {
    return {
        name: 'copy-to-ui',
        closeBundle() {
            const sourceDir = path.resolve('dist');
            const targetDir = path.resolve('../assets/ui');
            
            console.log('\n🚀 开始复制构建文件到ui目录...');
            
            try {
                // 检查源目录
                if (!fs.existsSync(sourceDir)) {
                    console.error('❌ 构建目录不存在');
                    return;
                }
                
                // 清空并创建目标目录
                if (fs.existsSync(targetDir)) {
                    fs.rmSync(targetDir, { recursive: true, force: true });
                }
                fs.mkdirSync(targetDir, { recursive: true });
                
                // 复制文件
                copyDir(sourceDir, targetDir);
                
                // 统计文件
                const files = getAllFiles(targetDir);
                
                console.log('✅ 文件复制完成！');
                console.log(`📂 目标目录: ${targetDir}`);
                console.log(`📊 共复制 ${files.length} 个文件\n`);
                
            } catch (error) {
                console.error('❌ 复制过程中出现错误:', error.message);
            }
        }
    };
}

/**
 * 递归复制目录
 */
function copyDir(src, dest) {
    const entries = fs.readdirSync(src, { withFileTypes: true });
    
    for (const entry of entries) {
        const srcPath = path.join(src, entry.name);
        const destPath = path.join(dest, entry.name);
        
        if (entry.isDirectory()) {
            fs.mkdirSync(destPath, { recursive: true });
            copyDir(srcPath, destPath);
        } else {
            fs.copyFileSync(srcPath, destPath);
        }
    }
}

/**
 * 获取目录下所有文件
 */
function getAllFiles(dir) {
    const files = [];
    
    function traverse(currentDir) {
        const entries = fs.readdirSync(currentDir, { withFileTypes: true });
        
        for (const entry of entries) {
            const fullPath = path.join(currentDir, entry.name);
            
            if (entry.isDirectory()) {
                traverse(fullPath);
            } else {
                files.push(fullPath);
            }
        }
    }
    
    traverse(dir);
    return files;
}