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
    const successMessage = Selector('a.contest-list-title').withText('test4');
    const virtualJoinButton = Selector('input.contest-join').withAttribute('value', 'Virtual join');
    const searchInput = Selector('#search');

    await t
        .typeText(usernameInput, 'admin')
        .typeText(passwordInput, 'Ducanh12a1@!')
        .click(loginButton)
        .expect(contestButton.exists).ok('Contests button should be visible after login')
        .click(contestButton)
        .expect(searchInput.exists).ok('Search input should be visible on the contest page')
        .click(searchInput)
        .typeText(searchInput, 'test4')
        .expect(successMessage.exists).ok('Should show contest block for test4 after searching');
});

