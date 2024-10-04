import { MainPage } from "../page_objects/test.page";
import { test as base } from "@playwright/test";


type PageFixture = {
    mainPage: MainPage;
    uuidPattern: RegExp;
}

export const test = base.extend<PageFixture>({
    mainPage: async ({ page }, use) => {
        const mainPage = new MainPage(page);
        await use(mainPage);
    },

    // Define the regex pattern for UUIDs
    uuidPattern: /\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b/i
})

export { expect } from "@playwright/test";