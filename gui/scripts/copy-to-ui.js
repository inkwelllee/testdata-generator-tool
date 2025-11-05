import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// 源目录和目标目录
const sourceDir = path.join(__dirname, '../dist');
const targetDir = path.join(__dirname, '../../asserts/ui');

/**
 * 递归复制目录
 * @param {string} src 源目录
 * @param {string} dest 目标目录
 */
function copyDir(src, dest) {
    try {
        // 确保目标目录存在
        if (!fs.existsSync(dest)) {
            fs.mkdirSync(dest, { recursive: true });
        }

        // 读取源目录
        const entries = fs.readdirSync(src, { withFileTypes: true });

        for (const entry of entries) {
            const srcPath = path.join(src, entry.name);
            const destPath = path.join(dest, entry.name);

            if (entry.isDirectory()) {
                // 递归复制子目录
                copyDir(srcPath, destPath);
            } else {
                // 复制文件
                fs.copyFileSync(srcPath, destPath);
            }
        }
    } catch (error) {
        console.error(`复制失败: ${error.message}`);
        process.exit(1);
    }
}

/**
 * 清空目标目录
 * @param {string} dir 要清空的目录
 */
function clearDir(dir) {
    try {
        if (fs.existsSync(dir)) {
            fs.rmSync(dir, { recursive: true, force: true });
        }
        fs.mkdirSync(dir, { recursive: true });
    } catch (error) {
        console.error(`清空目录失败: ${error.message}`);
        process.exit(1);
    }
}

// 主执行函数
function main() {
    console.log('🚀 开始复制构建文件到ui目录...');
    
    // 检查源目录是否存在
    if (!fs.existsSync(sourceDir)) {
        console.error('❌ 构建目录不存在，请先运行 npm run build');
        process.exit(1);
    }

    try {
        // 清空目标目录
        console.log('🧹 清空目标目录...');
        clearDir(targetDir);

        // 复制文件
        console.log('📁 复制文件...');
        copyDir(sourceDir, targetDir);

        console.log('✅ 文件复制完成！');
        console.log(`📂 源目录: ${sourceDir}`);
        console.log(`📂 目标目录: ${targetDir}`);
        
        // 显示复制的文件统计
        const files = getAllFiles(targetDir);
        console.log(`📊 共复制 ${files.length} 个文件`);
        
    } catch (error) {
        console.error('❌ 复制过程中出现错误:', error.message);
        process.exit(1);
    }
}

/**
 * 获取目录下所有文件
 * @param {string} dir 目录路径
 * @returns {string[]} 文件路径数组
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

// 执行主函数
main();