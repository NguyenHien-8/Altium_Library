package altium.migrator.service;

import lombok.SneakyThrows;
import lombok.extern.slf4j.Slf4j;
import org.apache.commons.io.FileUtils;
import org.eclipse.jgit.api.Git;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

import java.io.File;

@Slf4j
@Service
public class GitRepositoryService {

    @Value("${git.repository.url}")
    private String gitRepositoryUrl;

    @Value("${git.repository.branch:master}")
    private String gitRepositoryBranch;

    @Value("${git.repository.directory.name}")
    private String gitDirectoryName;

    @Value("${migration.root.folder}")
    private String destinationPath;

    @SneakyThrows
    public void cloneRepositoryWithChangelog() {
        File destinationDirectory = new File(destinationPath);

        if (!FileUtils.isEmptyDirectory(destinationDirectory)) {
            log.info("Destination directory {} is not empty. Skipping repository clone.", destinationPath);
            return;
        }

        String remoteBranch = "origin/" + gitRepositoryBranch;
        String branchRef = "refs/heads/" + gitRepositoryBranch;

        log.info(
                "Accessing git repository: {} (branch: {}, path: {})",
                gitRepositoryUrl,
                gitRepositoryBranch,
                gitDirectoryName
        );

        try (Git git = Git.cloneRepository()
                .setURI(gitRepositoryUrl)
                .setDirectory(destinationDirectory)
                .setBranch(branchRef)
                .setCloneAllBranches(false)
                .setCloneSubmodules(true)
                .setNoCheckout(true)
                .call()) {

            git.checkout()
                    .setStartPoint(remoteBranch)
                    .addPath(gitDirectoryName)
                    .call();
        }

        log.info(
                "Git repository successfully cloned to path: {} from branch: {}",
                destinationDirectory.getPath(),
                gitRepositoryBranch
        );
    }
}
