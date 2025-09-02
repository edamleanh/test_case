import { Selector } from 'testcafe';
const { BASE_URL } = require('../store');

fixture`Demo Login Test`
    .page`${BASE_URL}/accounts/login/`;

test('User can log in with valid credentials', async t => {
    const usernameInput = Selector('#id_username');
    const passwordInput = Selector('#id_password');
    const loginButton = Selector('button[type="submit"]');
    const contestButton = Selector('a.nav-contest');
    const successMessage = Selector('h2').withText('Problems');
    const contestLink = Selector('a.contest-list-title').withText('Test3');
    const virtualJoinButton = contestLink.parent('div').parent('td').sibling('td').find('input[type="submit"][value="Virtual join"]');
    const accessCodeInput = Selector('#id_access_code');
    const joinContestButton = Selector('button').withText('Join Contest');

    await t
        .expect(contestButton.exists).ok('Contests button should be visible after login')
        .click(contestButton)
        .expect(contestLink.exists).ok('Contest link should be visible')
        .expect(virtualJoinButton.exists).ok('Virtual join button for Test3 should be visible')
        .expect(virtualJoinButton.hasAttribute('disabled')).notOk('Virtual join button for Test3 should be enabled')
        .click(virtualJoinButton)
        .typeText(usernameInput, 'edamleanh')
        .typeText(passwordInput, 'Ducanh12a1@!')
        .click(loginButton)
        .typeText(accessCodeInput, '123456')
        .click(joinContestButton)
        .expect(successMessage.exists).ok('Should show contest banner after clicking contest link');
});
