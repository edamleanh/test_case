import { Selector } from 'testcafe';
const { BASE_URL } = require('../store');

fixture`Demo Login Test`
    .page`${BASE_URL}/accounts/login/`;

test('User can log in with valid credentials', async t => {
    const usernameInput = Selector('#id_username');
    const passwordInput = Selector('#id_password');
    const loginButton = Selector('button[type="submit"]');
    const contestButton = Selector('a.nav-contest');
    const contestLink = Selector('a.contest-list-title').withText('Test2');
    const successMessage = Selector('#banner a.date').withText('Contest is over.');
    const virtualJoinButton = Selector('input.contest-join').withAttribute('value', 'Virtual join');

    await t
        .expect(contestButton.exists).ok('Contests button should be visible after login')
        .click(contestButton)
        .expect(contestLink.exists).ok('Contest link should be visible')
        .click(contestLink)
        .expect(successMessage.exists).ok('Should show contest banner after clicking contest link');
});
