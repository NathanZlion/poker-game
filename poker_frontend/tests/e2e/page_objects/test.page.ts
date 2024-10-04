import { Page } from "@playwright/test";


// This is the main page
export class MainPage {
    constructor(private page: Page) { }

    async goto() {
        await this.page.goto('/');
    }

    async startGame() {
        const startBtn = this.page.getByTestId("setup.start-btn");
        await startBtn.click();
    }

    async performFold() {
        const foldBtn = this.page.getByTestId("actions.fold-btn");
        await foldBtn.click();
    }

    async performCheck() {
        const checkBtn = this.page.getByTestId("actions.check-btn");
        await checkBtn.click();
    }

    async performCall() {
        const callBtn = this.page.getByTestId("actions.call-btn");
        await callBtn.click();
    }

    async decreaseBetSize() {
        const decreaseBetBtn = this.page.getByTestId("actions.decrease-bet-btn");
        await decreaseBetBtn.click();
    }
    
    async performBet() {
        const betBtn = this.page.getByTestId("actions.bet-btn");
        await betBtn.click();
    }
    
    async increaseBetSize() {
        const increaseBetBtn = this.page.getByTestId("actions.increase-bet-btn");
        await increaseBetBtn.click();
    }

    async decreaseRaiseSize() {
        const decreaseRaiseBtn = this.page.getByTestId("actions.decrease-raise-btn");
        await decreaseRaiseBtn.click();
    }

    async performRaise() {
        const raiseBetBtn = this.page.getByTestId("actions.raise-btn");
        await raiseBetBtn.click();
    }

    async increaseRaiseSize() {
        const increaseRaiseBtn = this.page.getByTestId("actions.increase-raise-btn");
        await increaseRaiseBtn.click();
    }

    async setStack(stackAmount: string) {
        const stackInput = this.page.getByTestId("setup.stack-size-input");
        await stackInput.fill(stackAmount);
    }

    async getLogs(): Promise<string[]> {
        return await this.page.locator('#play-logs-wrapper p.block').allTextContents();
    }

    /// This waits for the logs to change
    async waitForLogsToChange(logBefore: string[]) {
        await this.page.waitForFunction(
            (logBefore) => {
                const currentLogs = Array.from(document.querySelectorAll('#play-logs-wrapper p.block')).map(log => log.textContent);
                return JSON.stringify(currentLogs) !== JSON.stringify(logBefore); // Logs changed for the first time
            },
            logBefore
        );
    }

    async getHandHistoryLogs() : Promise<string[]> {
        return await this.page.locator('#hand-history-wrapper p').allTextContents();
    }

    async waitForHandHistoryToChange(historyBefore: string[]) {
        await this.page.waitForFunction(
            (historyBefore) => {
                const currentHistory = Array.from(document.querySelectorAll('#hand-history-wrapper p')).map(log => log.textContent);
                return JSON.stringify(currentHistory) !== JSON.stringify(historyBefore); // history changes
            },
            historyBefore
        );
    }

    async getBetSize() : Promise<number> {
        const betBtn = this.page.getByTestId("actions.bet-btn");
        const content = await betBtn.textContent();
        const [_, amount] = content!.split(" ");

        return parseInt(amount);
    }

    async getRaiseSize(): Promise<number> {
        const raiseBtn = this.page.getByTestId("actions.bet-btn");
        const content = await raiseBtn.textContent();
        const [_, amount] = content!.split(" ");

        return parseInt(amount);
    }

    /// This is a test game play to test game completion
    async playGameToCompletion() {
        await this.startGame();

        let logs = await this.getLogs();
        let handHisoryLogs = await this.getHandHistoryLogs();


        // Let all other players fold and the one player win
        for (let i = 0; i < 5; i ++){
            logs = await this.getLogs();
            await this.performFold();
            await this.waitForLogsToChange(logs); // loading
            logs = await this.getLogs();
            await this.waitForLogsToChange(logs); // action performed
        }

        await this.waitForHandHistoryToChange(handHisoryLogs);
    }
}