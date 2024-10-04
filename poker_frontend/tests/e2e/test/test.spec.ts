import { test, expect } from '../fixtures/test.fixtures';


test.beforeEach(async ({ mainPage }) => {
    await mainPage.goto();
});


test.describe('UI Elements Tests', () => {
    test('has necessary elements', async ({ page }) => {
        await expect(page.getByTestId("playing-field-log-title")).toBeVisible();
        await expect(page.getByTestId("setup.stack-title")).toBeVisible();
        await expect(page.getByTestId("hand-history-title")).toBeVisible();
        await expect(page.getByTestId("setup.apply-btn")).toBeVisible();
        await expect(page.getByTestId("setup.start-btn")).toBeVisible();

        await expect(page.getByTestId("setup.stack-title")).toHaveText('Stack');
        await expect(page.getByTestId("playing-field-log-title")).toHaveText('Playing Field Log');
        await expect(page.getByTestId("hand-history-title")).toHaveText('Hand History');
        await expect(page.getByTestId("setup.apply-btn")).toHaveText('Apply');
        await expect(page.getByTestId("setup.start-btn")).toHaveText('Start');  // initially should have text start

        await expect(page.getByTestId("actions.fold-btn")).toBeVisible();
        await expect(page.getByTestId("actions.check-btn")).toBeVisible();
        await expect(page.getByTestId("actions.call-btn")).toBeVisible();

        await expect(page.getByTestId("actions.decrease-bet-btn")).toBeVisible();
        await expect(page.getByTestId("actions.bet-btn")).toBeVisible();
        await expect(page.getByTestId("actions.increase-bet-btn")).toBeVisible();

        await expect(page.getByTestId("actions.decrease-raise-btn")).toBeVisible();
        await expect(page.getByTestId("actions.raise-btn")).toBeVisible();
        await expect(page.getByTestId("actions.increase-raise-btn")).toBeVisible();

        await expect(page.getByTestId("actions.allin-btn")).toBeVisible();
    });

    test('action buttons are disabled before starting hand', async ({ page }) => {
        await expect(page.getByTestId("actions.fold-btn")).toBeDisabled();
        await expect(page.getByTestId("actions.check-btn")).toBeDisabled();
        await expect(page.getByTestId("actions.call-btn")).toBeDisabled();
        await expect(page.getByTestId("actions.decrease-bet-btn")).toBeDisabled();

        await expect(page.getByTestId("actions.bet-btn")).toBeDisabled();
        await expect(page.getByTestId("actions.increase-bet-btn")).toBeDisabled();
        await expect(page.getByTestId("actions.decrease-raise-btn")).toBeDisabled();
        await expect(page.getByTestId("actions.raise-btn")).toBeDisabled();
        await expect(page.getByTestId("actions.increase-raise-btn")).toBeDisabled();
        await expect(page.getByTestId("actions.allin-btn")).toBeDisabled();
    });
});

test.describe('Action Buttons Tests', () => {

    test('should change start button text to reset when hand starts', async ({ page, mainPage }) => {
        await expect(page.getByTestId("setup.start-btn")).toHaveText('Start');  // initially should have text start
        await mainPage.startGame();
        await expect(page.getByTestId("setup.start-btn")).toHaveText('Reset');  // should change to restart when the hand starts
    });

    test('Appropriate action buttons are enabled when starting hand', async ({ page, mainPage }) => {
        await mainPage.startGame();

        // Buttons that should get enabled
        await expect(page.getByTestId("actions.fold-btn")).toBeEnabled();
        await expect(page.getByTestId("actions.call-btn")).toBeEnabled();
        await expect(page.getByTestId("actions.decrease-raise-btn")).toBeEnabled();
        await expect(page.getByTestId("actions.raise-btn")).toBeEnabled();
        await expect(page.getByTestId("actions.increase-raise-btn")).toBeEnabled();
        await expect(page.getByTestId("actions.allin-btn")).toBeEnabled();

        // Unallowed actions should stay disabled
        await expect(page.getByTestId("actions.check-btn")).toBeDisabled();

        await expect(page.getByTestId("actions.decrease-bet-btn")).toBeDisabled();
        await expect(page.getByTestId("actions.bet-btn")).toBeDisabled();
        await expect(page.getByTestId("actions.increase-bet-btn")).toBeDisabled();
    });
});

test.describe('Play Logs Tests', () => {
    test('logs change when starting hand', async ({ mainPage }) => {

        const initialLogs = await mainPage.getLogs();
        expect(initialLogs[0]).toBe('Game not started.');

        await mainPage.startGame();

        await mainPage.waitForLogsToChange(initialLogs);
        const updatedLogs = await mainPage.getLogs();

        expect(updatedLogs).not.toEqual(initialLogs);
    });


    test('loading indicator appears in logs when a valid action btn is pressed', async ({ mainPage }) => {
        await mainPage.startGame();
        const initialLogs = await mainPage.getLogs();

        await mainPage.performCall();
        await mainPage.waitForLogsToChange(initialLogs);

        const updatedLogs = await mainPage.getLogs();

        expect(updatedLogs).not.toEqual(initialLogs);
        expect(updatedLogs[updatedLogs.length - 1]).toEqual("...");
    });


    test('logs change when a valid action gets completed', async ({ mainPage }) => {

        await mainPage.startGame();
        const initialLogs = await mainPage.getLogs();
        await mainPage.performCall();

        await mainPage.waitForLogsToChange(initialLogs);

        const firstUpdateLogs = await mainPage.getLogs();
        expect(firstUpdateLogs[firstUpdateLogs.length - 1]).toEqual("...");
        await mainPage.waitForLogsToChange(firstUpdateLogs);

        const secondUpdateLogs = await mainPage.getLogs();

        expect(secondUpdateLogs).not.toEqual(firstUpdateLogs);
        expect(secondUpdateLogs[secondUpdateLogs.length - 1]).not.toEqual("...");
    });


    test('Logs Hand Id when game played to end', async ({ mainPage, uuidPattern }) => {
        await mainPage.playGameToCompletion();
        const logs = await mainPage.getLogs();

        const logWithHandId = logs[logs.length - 2];
        const match = logWithHandId.match(uuidPattern);

        expect(match).not.toBeNull();
    });
});

test.describe('Hand History Tests', () => {
    test('History Should be added to the history when hand is completed', async ({ mainPage, uuidPattern }) => {
        const handHistoriesBeforeGamePlay = await mainPage.getHandHistoryLogs();
        await mainPage.playGameToCompletion();
        const logs = await mainPage.getLogs();
        const handHistoriesAfterGamePlay = await mainPage.getHandHistoryLogs();

        const logWithHandId = logs[logs.length - 2];
        const match = logWithHandId.match(uuidPattern);

        expect(match).not.toBeNull();
        const currentHandUUID = match![0];

        expect(handHistoriesAfterGamePlay.length).toBeGreaterThan(handHistoriesBeforeGamePlay.length)
        expect(handHistoriesAfterGamePlay[0]).toEqual(`Hand #${currentHandUUID}`);
    });
});
