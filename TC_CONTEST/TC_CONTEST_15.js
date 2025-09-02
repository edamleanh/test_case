import { Selector } from 'testcafe';
//run in 2 terminal
const { BASE_URL } = require('../store');

fixture`Demo Login Test`
    .page`${BASE_URL}/accounts/login/`;

test('User can log in with valid credentials', async t => {
    const usernameInput = Selector('#id_username');
    const passwordInput = Selector('#id_password');
    const loginButton = Selector('button[type="submit"]');
    const contestButton = Selector('a.nav-contest');
    const contestLink = Selector('a.contest-list-title').withText('Test2');
    const successMessage = Selector('#contest-info a').withText('Test2 -');
    const virtualJoinButton = Selector('input.contest-join').withAttribute('value', 'Virtual join');

    await t
        .typeText(usernameInput, 'admin')
        .typeText(passwordInput, 'Ducanh12a1@!')
        .click(loginButton)
        .expect(contestButton.exists).ok('Contests button should be visible after login')
        .click(contestButton)
        .expect(contestLink.exists).ok('Contest link should be visible')
        .click(contestLink)
        .expect(virtualJoinButton.exists).ok('Virtual join button should be visible')
        .click(virtualJoinButton)
        .expect(successMessage.exists).ok('Should show contest banner after clicking contest link');
    // Simulate closing the tab by navigating away
    await t
        .navigateTo('http://localhost:8000/contests/')
        .expect(contestLink.exists).ok('Contest link should be visible')
        .click(contestLink)
            .expect(successMessage.exists).ok('Should show contest banner after clicking contest link');
});
