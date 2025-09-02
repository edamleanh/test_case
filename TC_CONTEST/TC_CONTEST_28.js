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
    const contestLink1 = Selector('a.contest-list-title').withText('test10');
    const virtualJoinButton = Selector('input.contest-join').withAttribute('value', 'Virtual join');


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
        .expect(contestButton.exists).ok('Contests button should be visible after login')
        .click(contestButton)
        .expect(contestLink1.exists).ok('Contest link should be visible')
        .click(contestLink1)
        .wait(10000)
        .expect(virtualJoinButton.exists).ok('Virtual join button should be visible')
        .click(virtualJoinButton)

});
