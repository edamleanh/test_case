import { Selector } from 'testcafe';
//run in 2 terminal
const { BASE_URL } = require('../store');

fixture`Demo Login Test`
    .page`${BASE_URL}`;

test('User can log in with valid credentials', async t => {
    const loginButton = Selector('button[type="submit"]');
    const contestButton = Selector('a.nav-contest');
    const startTime = Date.now();
    await t
        .expect(contestButton.exists).ok('Contests button should be visible after login')
        .click(contestButton);

    const endTime = Date.now();
    const loadTime = endTime - startTime;
    console.log('Contest page load time (ms):', loadTime);
    await t.expect(loadTime).lte(1000, 'Contest page should load in less than 0.5 seconds');

});
