const vscode = require('vscode');
const { CodeAnalysisAgent } = require('./CodeAnalysisAgent');

function activate(context) {
    const agent = new CodeAnalysisAgent('your_openai_api_key');

    let disposable = vscode.commands.registerCommand('my-extension.analyzeCode', async () => {
        const editor = vscode.window.activeTextEditor;
        if (editor) {
            const code = editor.document.getText();
            const [updatedCode, issues, improvements] = await agent.run(code, 'Analyze the code');

            // Display the results in the VS Code UI
            vscode.window.showInformationMessage('Code analysis complete');
            vscode.window.showQuickPick(issues, { title: 'Code Issues' });
            vscode.window.showQuickPick(improvements, { title: 'Suggested Improvements' });
            editor.edit(editBuilder => {
                editBuilder.replace(new vscode.Range(0, 0, editor.document.lineCount, 0), updatedCode);
            });
        }
    });

    let addFunctionalityDisposable = vscode.commands.registerCommand('my-extension.addFunctionality', async () => {
        const editor = vscode.window.activeTextEditor;
        if (editor) {
            const code = editor.document.getText();
            const request = await vscode.window.showInputBox({ prompt: 'Enter the functionality you want to add:' });
            const updatedCode = await agent.add_functionality(code, request);

            // Replace the existing code with the updated code
            editor.edit(editBuilder => {
                editBuilder.replace(new vscode.Range(0, 0, editor.document.lineCount, 0), updatedCode);
            });
        }
    });

    context.subscriptions.push(disposable, addFunctionalityDisposable);
}

function deactivate() {}

module.exports = {
    activate,
    deactivate
};
