import { Selector } from 'testcafe';
const { BASE_URL } = require('../store');

fixture`Demo Login Test`
    .page`${BASE_URL}/accounts/login/`;

test('User can log in with valid credentials', async t => {
    const contestButton = Selector('a.nav-contest');
    const contestLink = Selector('a.contest-list-title').withText('Test');
    const successMessage = Selector('#banner a.date').withText('Starting in');

    await t
        .expect(contestButton.exists).ok('Contests button should be visible after login')
        .click(contestButton)
        .expect(contestLink.exists).ok('Contest link should be visible')
        .click(contestLink)
        .expect(successMessage.exists).ok('Should show contest banner after clicking contest link');
});
