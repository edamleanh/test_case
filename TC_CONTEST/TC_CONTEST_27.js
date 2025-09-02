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
    const virtualJoinButton = Selector('input.contest-join').withAttribute('value', 'Virtual join');
    const leaveContestButton = Selector('input.leaving-forever').withAttribute('value', 'Leave contest');
    const contestInfoLink = Selector('#contest-info a').withText('Test2 -');

    await t
        .typeText(usernameInput, 'edamleanh')
        .typeText(passwordInput, 'Ducanh12a1@!')
        .click(loginButton)
        .expect(contestButton.exists).ok('Contests button should be visible after login')
        .click(contestButton)
        .expect(contestLink.exists).ok('Contest link should be visible')
        .click(contestLink)
        .expect(virtualJoinButton.exists).ok('Virtual join button should be visible')
        .click(virtualJoinButton)
        .expect(contestInfoLink.exists).ok('Contest info link should be visible')
        .click(contestInfoLink)
        .expect(leaveContestButton.exists).ok('Leave contest button should be visible')
        .click(leaveContestButton)
        .expect(virtualJoinButton.exists).ok('Virtual join button should be visible');
});
