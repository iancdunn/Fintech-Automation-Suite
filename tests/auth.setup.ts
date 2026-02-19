import {test as setup} from '../fixtures/pom-fixtures';
import path from 'path';

const users = ['demo1', 'demo2', 'demo3', 'demo4'];

for(const user of users){
    setup(`authenticate ${user}`, async ({page, loginPage})=>{
        await loginPage.goto();
        await loginPage.login(user, 'password123');
        await page.waitForURL('/');

        await page.context().storageState({path: `playwright/.auth/${user}.json`});
    });
}